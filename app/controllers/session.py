from .base import Base


class Session(Base):

    async def _post(self):
        """ This is a user signin request handler """
