import pytest
import asyncio

from ..utils.db_connect import db_connector, drop_schema
from ..settings import DB_CONFIGS

@pytest.fixture(scope='session')
def configure_db():
    drop_schema(**DB_CONFIGS['test'])
    conn = db_connector('test')
    yield conn
    conn.close()

@pytest.fixture(scope='module')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def connect_client():
    def connect(host='localhost', port=8080):
        return asyncio.open_connection(host=host, port=port)
    return connect

@pytest.fixture
def disconnect_client():
    async def disconnect(pipe):
        pipe.close()
        await pipe.wait_closed()
    return disconnect
