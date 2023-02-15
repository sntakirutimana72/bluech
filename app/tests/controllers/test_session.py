import pytest
import json

from ..support.unittests import PyTestCase

@pytest.mark.usefixtures('configure_db', 'server', 'clis_con')
class TestSession(PyTestCase):
    @pytest.mark.asyncio
    async def test_signin(self):
        signin_req = {
            'content_length': int,
            'content_type': 'json',
            'protocol': 'signin',
            'request': {
                'body': {
                    'user': {
                        'email': 'admin@email.com',
                        'password': 'test@123'
                    }
                }
            }
        }
        # formatting data and packing it for a specific factory pattern recognizable by the server
        to_json = json.dumps(signin_req)
        to_bytes = to_json.encode()
        c_len = str(len(to_bytes)).encode()
        payload = c_len + to_bytes
        self._writer.write(payload)
        await self._writer.drain()

    @pytest.mark.asyncio
    async def test_signout(self):
        ...
