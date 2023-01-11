from .serializers import decompress, compress

async def fetch(reader):
    data = await reader.read()
    return decompress(data)

async def pump(writer, data):
    writer.write(compress(data))
    await writer.drain()
