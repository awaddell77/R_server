#server connection
#will start as a wrapper of sorts of socket connections
#custom methods will be added as needed
import socket
class Serv_connection:
	def __init__(self, connection):
		if isinstance(connection, socket.socket): self.connection = connection
		else: raise TypeError("Connection must be socket")
	def receive(self, buffer_size=1024):
		mess = self.connection.recv(buffer_size)
		return mess
	def send(self,mess, encoding = 'ascii'):
		self.connection.send(bytes(str(mess), encoding))
		return
	def close(self):
		self.connection.close()
		return



