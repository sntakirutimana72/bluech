from .base import Base
from ..utils.sql import SessionQueryManager

class Session(Base):
    async def _post(self):
        """ Signin """
        return SessionQueryManager.signin(**self._request.body.user)

    async def _delete(self):
        """ Signout """
        SessionQueryManager.signout(self.user_id)
