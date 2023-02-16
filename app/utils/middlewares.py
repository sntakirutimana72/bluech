from .processor import Processor

async def accept_conn(reader, writer):
    # Start the processing phase of the client connection
    # Initiate an instance of Processor
    Processor(reader, writer)
