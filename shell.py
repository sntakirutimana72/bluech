import asyncio

loop = asyncio.new_event_loop()

try:
    loop.run_forever()
except:
    ...
