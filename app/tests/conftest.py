import pytest

from ..utils.db_connect import db_connector, drop_schema
from ..settings import DB_CONFIGS

@pytest.fixture(scope='session')
def configure_db():
    drop_schema(**DB_CONFIGS['test'])
    conn = db_connector('test')
    yield conn
    conn.close()
