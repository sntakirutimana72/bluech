from .base import Base
from ..utils import sql
from ..utils.pipe import create_response_task

class Groups(Base):
    
    async def _post(self):
        """Create a new group"""
        
    async def _put(self):
        """Add new member in the group"""
        
    async def _pop(self):
        """Remove a group member"""
        
    async def _drop(self):
        """Exit group"""
        
    async def _delete(self):
        """Delete a group"""
    