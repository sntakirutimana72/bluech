from .processors import AuthProcessor

def service_connection(db):
    async def middleware(reader, writer):
        # Authenticate a first time accepted client connection.
        is_auth, reason = await AuthProcessor(reader, db).process()
        # Assert authentication feedback
        if is_auth:
            ...
        else:
            ...
