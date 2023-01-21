import peewee as pee
import psycopg2

from ..settings import DB_CONFIGS
from ..models import *

def db_connector(env='development'):
    """ Used to set up and load database initial configuration on start-up. """
    # Ready options
    options = DB_CONFIGS[env].copy()
    schema = options.pop('schema')
    # Ensure schema exists
    _ = psycopg2.connect(**options)
    _.cursor().execute(f'CREATE DATABASE {schema!r}')
    _.close()
    # Create a db instance with specific configurations
    database = pee.PostgresqlDatabase(schema, **options)
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
