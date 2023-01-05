# Database environment variables

#:=>default

DB_DEFAULT = {
    host: 'localhost',
    port: 5542,
    user: 'postgres',
    password: 'postgres'
}

#:=>development, :=>test, :=>production

DB_CONFIGS = {
    'development': {
        schema: 'bluech_development',
        **DB_DEFAULT
    },
    'test': {
        schema: 'bluech_test',
        **DB_DEFAULT
    },
    'production': {
        schema: 'bluech_production',
        **DB_DEFAULT
    }
}
