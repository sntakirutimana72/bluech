from .serializers import decompress, compress
from .shareables import tasks_Q
from .interfaces import AttributeDict

async def fetch(reader):
    data = await reader.read()
    return decompress(data)

async def pump(writer, data):
    writer.write(compress(data))
    await writer.drain()

async def create_response_task(proto, resource_id, **options):
    tasks_q = tasks_Q()
    await tasks_q.push(AttributeDict({**options, 'proto': proto, 'id': resource_id}))
