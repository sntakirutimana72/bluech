from .interfaces import AttributeDict
from ..settings import ALLOWED_ROUTES

def router(name, controller):
    return AttributeDict({'url': ALLOWED_ROUTES[name], 'controller': controller})
