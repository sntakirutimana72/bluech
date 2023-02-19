from typing import Any, Callable

from .interfaces import AttributeDict
from ..settings import ALLOWED_ROUTES

def router(name: str, controller: Callable) -> AttributeDict[str, Any]:
    return AttributeDict({'url': ALLOWED_ROUTES[name], 'controller': controller})
