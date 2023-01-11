from peewee import PostgresqlDatabase

from ..settings import DB_CONFIGS
from ..models import *


def db_connector(env='development'):
    """ Used to set up and load database initial configuration on start-up. """
    # Create a db instance with specific configurations
    database = PostgresqlDatabase(**DB_CONFIGS[env])
    # Initiate db instance connection
    database.connect(reuse_if_open=True)
    # Contain all models into one re-usable variable
    models = [
        User,
        Privilege,
        UserPrivilege,
        Action,
        Resource,
        Message,
        Group,
        Joint,
        Log
    ]
    # Bind models the current db connection instance
    database.bind(models, bind_refs=False, bind_backrefs=False)
    # Create model tables in the db schema
    database.create_tables(models, safe=True)

    return database
