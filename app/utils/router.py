from typing import Union, List, Tuple

from .interfaces import AttributeDict
from ..settings import ALLOWED_ROUTES

def router(args: Union[Tuple[str], List[str], str], controller) -> Union[AttributeDict, List[AttributeDict]]:
    if isinstance(args, (list, tuple,)):
        return [
            router(name, controller) for name in args
        ]
    return AttributeDict({'url': ALLOWED_ROUTES[args], 'controller': controller})
