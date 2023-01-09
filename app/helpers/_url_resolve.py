class Route:

    def __init__(url, handler, name):
        self.url = url
        self.handler = handler
        self.name = name
        
def route(url, controller, name=None):
    return Route(url, controller, name)
