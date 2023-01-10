from .interfaces import AttributeDict

def router(url, controller):
    return AttributeDict({'url': url, 'controller': controller})
