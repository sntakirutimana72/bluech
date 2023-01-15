from functools import lru_cache

from .db_connect import db_connector
from .interfaces import ChannelsQ, Queuable

@lru_cache(typed=True)
def db_conn(env='development'):
    return db_connector(env)

@lru_cache
def channels_Q():
    return ChannelsQ()

@lru_cache
def tasks_Q():
    return Queuable()
