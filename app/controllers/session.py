from .base import Base
from ..utils import sql

class Session(Base):

    async def _post(self):
        """ Signin """
        return sql.signin(self._request.body['name'])
        
    async def _delete(self):
        """ Signout """
        sql.signout(self.user_id)
