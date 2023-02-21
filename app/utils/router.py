import typing as yi

from .interfaces import AttributeDict
from ..settings import ALLOWED_ROUTES

def router(name: str | list[str], controller: yi.Callable):
    if type(name) is list:
        return [router(single, controller) for single in name]
    return AttributeDict({'url': ALLOWED_ROUTES[name], 'controller': controller})
