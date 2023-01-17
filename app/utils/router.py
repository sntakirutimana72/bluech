from typing import Any, Callable

from .interfaces import AttributeDict
from ..settings import ALLOWED_ROUTES

def router(args: str | tuple | list, controller: Callable) -> AttributeDict[str, Any] | list[AttributeDict[str, Any]]:
    if isinstance(args, (list, tuple,)):
        return [
            router(name, controller) for name in args
        ]
    return AttributeDict({'url': ALLOWED_ROUTES[args], 'controller': controller})
