from .utils.interfaces import AttributeDict
from .utils.working_dirs import WorkingDirs

# :APP_NAME
APP_NAME = 'bluech'

# Server environment
##
# :=>host IP
HOST_URL = 'localhost'
#
# :=>host PORT
HOST_PORT = 8090
#
# Pre-defined Allowed Routes
ALLOWED_ROUTES = AttributeDict({
    'signin': 'POST:/session',
    'signout': 'DELETE:/session',

    'all_messages': 'GET:/messages?recipient=<int>&page=<int>',
    'new_message': 'POST:/messages',
    'edit_message': 'PATCH:/messages/<id int>',
    'remove_message': 'DELETE:/messages/<id int>',

    'edit_username': 'PATCH:/users/<id int>',
    'change_user_avatar': 'PUT:/users/<id int>'
})


# Database environment variables
##
# :=>default
DB_DEFAULT = AttributeDict({
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'postgres'
})
#
# :=>development, :=>test, :=>production
DB_CONFIGS = AttributeDict({
    'development': AttributeDict({
        'schema': 'bluech_development',
        **DB_DEFAULT
    }),
    'test': AttributeDict({
        'schema': 'bluech_test',
        **DB_DEFAULT
    }),
    'production': AttributeDict({
        'schema': 'bluech_production',
        **DB_DEFAULT
    })
})

# Logging
#
# :=>db
LOGGING_LEVELS = AttributeDict({
    'LOGIN': 1,
    'LOGOUT': 2,
    'MSG_NEW': 3,
    'MSG_EDIT': 4,
    'MSG_DEL': 5,
    'MSG_ALL': 6,
    'USER_EDIT_NICKNAME': 7,
    'USER_EDIT_PIC': 8,
    'USERS_ALL': 9
})

# System Configurations
#
# :=>encoding
ENCODING = 'utf-8'
#
# :=>content-types
CONTENT_TYPES = [
    'application/json',
    *[f'image/{sx}' for sx in ('png', 'jpg', 'jpeg', 'gif')]
]

# Working dirs
#
#  :INSTALLED
INSTALLED_PATH = WorkingDirs.installed()

# :APPDATA
APPDATA_PATH = WorkingDirs.app_data(APP_NAME)

# :ASSETS_PATH
ASSETS_PATH = WorkingDirs.global_assets(APPDATA_PATH)

# :IMAGES_PATH
IMAGES_PATH = WorkingDirs.image_assets(ASSETS_PATH)

# :AVATARS_PATH
AVATARS_PATH = WorkingDirs.avatar_assets(IMAGES_PATH)
