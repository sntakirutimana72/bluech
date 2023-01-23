import pytest

from ..utils.db_connect import db_connector, drop_schema
from ..settings import DB_CONFIGS

@pytest.fixture
def configure_db():
    conn = db_connector('test')
    
    yield conn
    
    conn.close()
    
    options = DB_CONFIGS['test'].copy()
    schema = options.pop('schema')
    
    drop_schema(schema, **options)
