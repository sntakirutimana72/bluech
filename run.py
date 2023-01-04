if __name__ == '__main__:
    # definition scope for system environments
    
    # system bound imports
    import asyncio
    
    # local imports
    from .app.server import serve
    
    asyncio.run(serve(ip = 'localhost', port = 8080))
