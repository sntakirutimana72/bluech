#!/usr/bin/env python3

import asyncio
import logging
logging.basicConfig(level=logging.INFO)

def _DEFAULT_REPLY_CB(message):
	return message

class MockTCPServer:

	"""Implements a simple mock TCP server that responds to received
	messages. Closes the client socket after one message.

	By default, the server responds with a copy of the received message.
	Reply message can be customized using `reply_cb` callback function.
	This has to be a pure function that takes one input (input message)
	and outputs a reply to be sent to the client (preferably in bytes). 
	"""

	def __init__(self, port=8888, reply_cb=_DEFAULT_REPLY_CB, loop=None):
		self._port = port
		self._reply_cb = reply_cb
		self._loop = loop if loop != None else asyncio.get_event_loop()
		self._logger = logging.getLogger(self.__class__.__name__)

	def __await__(self):
		self._server = yield from asyncio.start_server(
			self.__on_message, host='127.0.0.1', port=self._port, loop=self._loop)
		
		self._logger.info('Listening on port %s' % self._port)
		return self

	async def __on_message(self, reader, writer):
		message = await reader.read(4096)
		self._logger.info(
			'Received message from "%s:%s"' % writer.get_extra_info('peername'))

		# Compute a reply message from provided `reply_cb` function
		reply = self._reply_cb(message)

		self._logger.info('Sending response...')
		writer.write(
			reply if type(reply) == bytes else reply.encode('ascii'))
		await writer.drain()

		self._logger.info('Closing the client socket...')
		writer.close()
	
	@property
	def port(self):
		return self._port

if __name__ == '__main__':
	"""Runs standalone as well."""
	try:
		loop = asyncio.get_event_loop()
		asyncio.ensure_future(MockTCPServer(), loop=loop)
		loop.run_forever()
	except KeyboardInterrupt:
		print('\nBye!')