import pytest
import requests

from ..support.mocks.servers import AppServerSpec
from ..support.mocks.clients import AppClientSpec
from ..support.unittests import PyTestCase
from ..support.models import create_user
from ...utils.interfaces import AttributeDict
from ...models import User, Activity, ActivityLog
from ...settings import LOGGING_LEVELS

@pytest.fixture(scope='module', autouse=True)
def logging_levels():
    Activity.insert_many([{'level': k} for k in LOGGING_LEVELS.values()]).execute()
    yield
    Activity.delete().execute()

@pytest.fixture(scope='class')
def server(event_loop):
    server = AppServerSpec()
    event_loop.run_until_complete(server.initiate())
    yield
    event_loop.run_until_complete(server.terminate())

@pytest.fixture
def user_avatar():
    url = 'https://www.w3schools.com/howto/img_avatar.png'
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        return AttributeDict({
            'content': resp.content,
            'content_type': resp.headers['Content-Type'],
            'content_length': int(resp.headers['Content-Length'])
        })

@pytest.mark.usefixtures('server')
class ControllerTestCases(PyTestCase):
    client: AppClientSpec
    signedIn: bool
    user: User
    avatar: AttributeDict

    @classmethod
    def setup_class(cls):
        cls.client = AppClientSpec()
        cls.signedIn = False
        cls.user = create_user()

    @classmethod
    def teardown_class(cls):
        delattr(cls, 'client')
        delattr(cls, 'signedIn')
        delattr(cls, 'user')

    async def assertSigninSuccess(self, **user):
        if self.signedIn:
            return
        resp = await self.assertSignin(self.client, user)
        self.signedIn = True
        return resp

    async def assertSignin(self, client: AppClientSpec, user: dict[str, str]):
        old_count = ActivityLog.select().count()
        resp = await client.login(**user)
        self.assertResponse(200, 'signin_success', resp)
        self.assert_equals(ActivityLog.select().count(), old_count + 1)
        self.assert_dict_has_key(resp, 'user')
        return resp

    def assertResponse(self, status: int, proto: str, resp):
        self.assert_isinstanceof(resp, dict)
        self.assert_dict_has_key(resp, 'proto')
        self.assert_equals(resp['proto'], proto)
        self.assert_dict_has_key(resp, 'status')
        self.assert_equals(resp['status'], status)
