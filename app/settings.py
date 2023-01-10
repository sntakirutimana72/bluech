from .utils.interfaces import AttributeDict

# Server environment
##
#:=>host IP
HOST_URL = 'localhost'
#
#:=>host PORT
HOST_PORT = 8090


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
