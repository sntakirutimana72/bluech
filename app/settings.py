from .utils.interfaces import AttributeDict

# Server environment
##
#:=>host IP
HOST_URL = 'localhost'
#
#:=>host PORT
HOST_PORT = 8090
#
# Pre defined Allowed Routes
ALLOWED_ROUTES = AttributeDict({
    # For session
    'signin': 'POST:/session',
    'signout': 'DELETE:/session',
    # For messages
    'all_messges': 'GET:/messages',
    'new_message': 'POST:/messages',
    'edit_messge': 'PATCH:/messages/<id int>',
    'remove_message': 'DELETE:/messages/<id int>',
    # For users
    'edit_username': 'PATCH:/users/<id int>',                        # (edit display name)
    'edit_profile_pic': 'PUT:/users/<id int>',                       # (change profile picture)
    'all_users': 'GET:/users',                                       # (fetch all users)
    # For groups
    'new_group': 'POST:/groups',                                     # (create group)
    'new_member': 'PUT:/groups/<id int>',                            # (add member)
    'remove_member': 'DELETE:/groups/<id int>/members/<id int>',     # (remove member)
    'exit_group': 'DROP:/groups/<id int>',                           # (leave group)
    'remove_group': 'DELETE:/groups/<id int>',                       # (delete group)
    'group_privilege': 'ASSIGN:/groups/<id int>/members/<id int>',   # (assign privilege)
    # For invalid routes
    'not_found': '*'
})


# Database environment variables
##
#:=>default
DB_DEFAULT = AttributeDict({
    host: 'localhost',
    port: 5542,
    user: 'postgres',
    password: 'postgres'
})
#
#:=>development, :=>test, :=>production
DB_CONFIGS = AttributeDict({
    'development': AttributeDict({
        schema: 'bluech_development',
        **DB_DEFAULT
    }),
    'test': AttributeDict({
        schema: 'bluech_test',
        **DB_DEFAULT
    }),
    'production': AttributeDict({
        schema: 'bluech_production',
        **DB_DEFAULT
    })
})


# System Configurations
#
#:=>encoding
ENCODING = 'utf-8'
#
# :=>content-types
CONTENT_TYPES = ('json', 'text',)
