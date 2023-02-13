import pytest

from ..support.unittests import PyTestCase

class TestSession(PyTestCase):

    @pytest.mark.asyncio
    async def test_signin(self, cli_con, cli_discon):
        reader, writer = await cli_con()
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
        writer.write(payload)
        await writer.drain()

    @pytest.mark.asyncio
    async def test_signout(self):
        ...
