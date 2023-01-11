from functools import lru_cache

from .db_connect import db_connector
from .interfaces import AttributeDict, Queuable

@lru_cache(typed=True)
def db_conn(env='development'):
    return db_connector(env)

@lru_cache
def conns_Q():
    return AttributeDict()

@lru_cache
def messages_Q():
    return Queuable()
