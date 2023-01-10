from ..urls import urls_patterns

def dispatch(url, **options):
    for route in urls_patterns[:-1]:
        if route.url == url:
            return route.controller(url, **options)
    return urls_patterns[-1].controller(url, **options)
    