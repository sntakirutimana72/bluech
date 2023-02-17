import pytest
import asyncio

from ..support.unittests import PyTestCase
from ...utils.layers import PipeLayer

@pytest.mark.usefixtures('configure_db', 'server')
class TestSession(PyTestCase):
    @pytest.mark.asyncio
    async def test_signin(self, cli_con):
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
        # connect to server
        reader, writer = await cli_con
        # formatting data and packing it for a specific factory pattern recognizable by the server
        await PipeLayer.pump(writer, signin_req)
        # pause for a minute for the transition to complete its course
        await asyncio.sleep(.25)
        # now, receive server response
        resp = await PipeLayer.fetch(reader)
        print(resp)

    @pytest.mark.asyncio
    async def test_signout(self):
        ...
