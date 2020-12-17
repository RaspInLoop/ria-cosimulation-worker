#!/usr/bin/env python
 
# This server demonstrates Thrift's connection 
 
port = 8100
 
import sys
# your gen-py dir
sys.path.append('./gen-py')
 
import time

 
from ril import *
from ril.ttypes import *
 
# Thrift files
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
 
from coSimulationHandler import CoSimulationHandler

# set handler to our implementation
handler = CoSimulationHandler()
 
processor = CoSimulation.Processor(handler)
transport = TSocket.TServerSocket("0.0.0.0", port)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
 
# set server
server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
 
print ('Starting server')
server.serve()