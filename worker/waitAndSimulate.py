from RedisQueue import RedisQueue
from os import environ
import json
from fmpy.ssp.simulation import simulate_ssp
import requests
import sys, traceback

class MessageProvider(object):
    def get_message():
        pass

class RedisMessageProvider(MessageProvider):
    def __init__(self, host, port, queue_name ):
        self.queue = RedisQueue( name=queue_name,
                    namespace='queue', 
                    host=host,
                    port=port)
        self.queue.wait_for()

    def get_message(self):
        return self.queue.get()

class FileMessageProvider(MessageProvider):
    def __init__(self, filename ):
        self.message_file =filename

    def get_message(self):
        with open(self.message_file, 'r') as file:
            return file.read()



oneshot_worker = ("ONE_SHOT" in environ)
if ("CLI_PROVIDED_MESSAGE" in environ):
    provider = FileMessageProvider(environ["CLI_PROVIDED_MESSAGE"])
    print(f"Started with FileMessageProvider with {environ['CLI_PROVIDED_MESSAGE']}") 
else:    
    redis_host =environ.get("REDIS_HOST", "localhost")
    redis_port = int(environ.get("REDIS_PORT", "6379"))
    print(f"Using RedisMessageProvider on {redis_host}:{redis_port}")  
    provider = RedisMessageProvider(redis_host, redis_port, environ.get("SIMULATION_WORK_QUEUE_NAME", "simulation_work"))   
    print(f"Started with RedisMessageProvider on {redis_host}:{redis_port}")     

def download_ssp_zip(ssp_uri):   
    try:
        print(f"Downloading {ssp_uri}")
        r = requests.get(ssp_uri, allow_redirects=True)
        open('file.ssp', 'wb').write(r.content)
        return 'file.ssp'
    except Exception as download_error:
        print(f"ERROR: Cannot download {ssp_uri}: {download_error}")


def set_simulation_env( envs):
    for var_name, endpoint in envs.items():
        host_var_name=var_name+"_HOST"        
        environ[host_var_name] = endpoint["host"]
        port_var_name=var_name+"_PORT"        
        environ[port_var_name] = str(endpoint["port"])

while True:
    print("Waiting for work")
    message=json.loads(provider.get_message())
    step_size=message['step-size']
    stop_time=message['stop-time']
    ssp_file=download_ssp_zip(message['ssp_uri'])
    set_simulation_env(message['fmu-environment'])
    print(f"Start co-simulation of {message['id']}")    
    try:
        simulate_ssp(ssp_file, step_size=step_size, stop_time=stop_time)
    except Exception as simulation_error:
        print(f"ERROR: Cannot co-simulate {message['id']} :  {simulation_error}")

    print(f"Co-simulation of {message['id']} done!")
    if (oneshot_worker):
        print("One shot! -> exiting")
        break

