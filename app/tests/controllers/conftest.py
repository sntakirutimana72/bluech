import pytest
import pathlib
import requests

from ..support.mocks.servers import AppServerSpec
from ..support.mocks.clients import AppClientSpec
from ..support.unittests import PyTestCase
from ...settings import APP_NAME

@pytest.fixture(scope='class')
def server(event_loop):
    server = AppServerSpec()
    event_loop.run_until_complete(server.initiate())
    yield
    event_loop.run_until_complete(server.terminate())
    
@pytest.fixture(scope='class')
def demo_avatar(request):
    url = 'https://www.w3schools.com/howto/img_avatar.png'
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        request.cls.avatar = resp.raw
    
@pytest.fixture(scope='class')
def prog_path(tmp_path_factory):
    return tmp_path_factory.mktemp(f'AppData/{APP_NAME}')

@pytest.fixture(scope='class')
def assets_path(prog_path):
    return prog_path.mkdir('assets')

@pytest.fixture(scope='class')
def images_path(assets_path):
    return assets_path.mkdir('images')

@pytest.fixture(scope='class')
def avatars_path(images_path):
    return images_path.mkdir('avatars')

@pytest.mark.usefixtures('server')
class ControllerTestCases(PyTestCase):
    client: AppClientSpec

    @classmethod
    def setup_class(cls):
        cls.client = AppClientSpec()
        cls.signedIn = False

    async def assertSigninSuccess(self, **user):
        if self.signedIn:
            return
        
        resp = await self.client.login(**user)
        self.assertResponse(200, 'signin_success', resp)
        self.assert_dict_has_key(resp, 'user')
        self.signedIn = True
        return resp

    def assertResponse(self, status: int, proto: str, resp):
        self.assert_isinstanceof(resp, dict)
        self.assert_dict_has_key(resp, 'proto')
        self.assert_equals(resp['proto'], proto)
        self.assert_dict_has_key(resp, 'status')
        self.assert_equals(resp['status'], status)
