# -*- coding: utf-8 -*-
"""
Created on Thu May 20 09:29:38 2021

@author: Vrushank Agrawal
"""

# --------------------------------------------------------------------
import asyncio

import telnetlib

with telnetlib.Telnet('localhost', 8888) as tn:
    tn.interact()

# --------------------------------------------------------------------
class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

# --------------------------------------------------------------------
loop   = asyncio.get_event_loop()
coro   = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass


