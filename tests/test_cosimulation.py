import pytest
import requests
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

pytest_plugins = ["docker_compose"]

token="f9403fc5f537b4ab332d"

# Invoking this fixture: 'function_scoped_container_getter' starts all services
@pytest.fixture(scope="function")
def wait_for_api(function_scoped_container_getter):
    """Wait for the api from my_api_service to become responsive"""
    request_session = requests.Session()
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])
    request_session.mount('http://', HTTPAdapter(max_retries=retries))

    service = function_scoped_container_getter.get("webserver").network_info[0]
    api_url = "http://%s:%s/" % (service.hostname, service.host_port)
    assert request_session.get(api_url)
    return request_session, api_url



def test_read_and_write(wait_for_api):
    """The Api is now verified good to go and tests can interact with it"""
    request_session, api_url = wait_for_api
    print(f'webserver for test running at {api_url}')
    files = {'file': open('outputs_inputs.json', 'rb')}
    request_session.put('%sfiles/upload?token=%s' % (api_url, filename, token), files)
    item = request_session.get('%sfiles/%s?token=%s' % (api_url, filename, token))
    assert item['data'] == data_string
    request_session.delete('%sfiles/%s?token=%s' % (api_url, filename, token))