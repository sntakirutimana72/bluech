import pytest
import platform
import asyncio as io

from ..utils.db_connect import db_connector, drop_schema
from ..settings import DB_CONFIGS
from .. import models

@pytest.fixture(scope='session')
def event_loop():
    if platform.system() == 'Windows':
        # As pytest with asyncio throws occasional RuntimeError('Event loop is closed') on Windows oses,
        # I'm setting windows loop event policy to avoid this issue.
        # It happens when working with sockets and streams
        io.set_event_loop_policy(io.WindowsSelectorEventLoopPolicy())
    loop = io.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope='session', autouse=True)
def configure_db():
    drop_schema(**DB_CONFIGS['test'])
    conn = db_connector('test')
    yield conn
    conn.close()

@pytest.fixture(scope='class', autouse=True)
def purge_db():
    yield
    for model_cls in map(models.__dict__.get, models.__all__):
        if model_cls.cls_name() in ('_model', 'activity'):
            continue
        model_cls.delete().execute()
