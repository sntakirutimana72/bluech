import pytest
import peewee as pee

from ..utils.db_connect import db_connector
from .. import models

@pytest.fixture(scope='session')
def configure_db():
    conn = db_connector('test')
    
    yield conn
    model_cls: list[pee.Model] = list(map(models.__dict__.get, models.__all__))  # type: ignore
    model_cls.reverse()
    
    for cls in model_cls:
        cls.truncate_table(restart_identity=True, cascade=True)
        
    conn.close()
