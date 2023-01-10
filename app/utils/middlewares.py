from .processor import Processor

async def accept_conn(reader, writer):
    # Invoke a lifetime copy of the processor to handle communication on both ends.
    Processor(reader, writer)
