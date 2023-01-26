import peewee as pee
import psycopg2

from ..settings import DB_CONFIGS
from ..models import *

def _init_conn(**options):
    con = psycopg2.connect(**options)
    con.set_session(autocommit=True)
    return con

# noinspection PyBroadException
def create_schema(schema, **options):
    con = None
    try:
        con = _init_conn(**options)
        con.cursor().execute(f'CREATE DATABASE {schema}')
    except:
        ...
    if con:
        con.close()

# noinspection PyBroadException
def drop_schema(schema, **options):
    con = None
    try:
        con = _init_conn(**options)
        con.cursor().execute(f'DROP DATABASE {schema}')
    except:
        ...
    if con:
        con.close()

def db_connector(env='development'):
    """ Used to set up and load database initial configuration on start-up. """
    # Ready options
    options = DB_CONFIGS[env].copy()
    schema = options.pop('schema')
    # Ensure schema exists
    create_schema(schema, **options)
    # Create a db instance with specific configurations
    database = pee.PostgresqlDatabase(schema, autorollback=True, **options)
    # Initiate db instance connection
    database.connect(reuse_if_open=True)
    # Contain all models into one re-usable variable
    models = [
        User,
        Channel,
        Member,
        Message,
        Resource,
        Activity,
        ActivityLog
    ]
    # Bind models the current db connection instance
    database.bind(models, bind_refs=False, bind_backrefs=False)
    # Create model tables in the db schema
    database.create_tables(models)

    return database
