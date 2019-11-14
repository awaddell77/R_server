#server connection
#will start as a wrapper of sorts of socket connections
#custom methods will be added as needed
#threaded
#TODO: REFACTOR reponse_queue since it is not a queue
import socket, datetime
from datetime import timezone
from threading import *
from w_csv import *

class S_connection(Thread):
	def __init__(self, connection, response_queue, log_info, lst_lock, resp_lock):
		super().__init__()
		if isinstance(connection, socket.socket): self.connection = connection
		else: raise TypeError("Connection must be socket")

		self.response_queue = response_queue
		self.resp_lock = resp_lock
		self.log_info = log_info
		self.lst_lock = lst_lock
	def receive_data(self, buffer_size=1024):
		mess = self.connection.recv(buffer_size)
		return mess
	def send_data(self,mess, encoding = 'ascii'):
		self.connection.send(bytes(str(mess), encoding))
		return
	def _logmsg(self, message):
		d_t = datetime.datetime.now(timezone.utc).isoformat()
		mess = d_t + ': '+ str(message)
		
		while self.lst_lock.locked():
			continue
		try:

			self.lst_lock.acquire()
			self.log_info.append(mess)
		except Exception as E:
			mess = d_t + ': ' + "ERROR: " + str(E)
			print("Problem locking")
			self.log_info.append(mess)
		finally:
			#print("lol")
			if self.lst_lock.locked(): self.lst_lock.release()


	
	def close_con(self):
		self.connection.close()
		return
	def receive_rep(self, chunk_size= 1024):
		pass
	def process_report_chunk(self, data, encoding = 'ascii'):
		pass
	def process_message(self):
		mess = self.receive_data()
		f_line = mess.find(b'\n')

		if mess[:f_line] == b'report': 
			self.send_data('hi', 'ascii')
			self._logmsg("Report Order received")
			#self.response_queue.add('Report order')
			res = self.receive_rep()
			
			self._logmsg("Returned {0} rows".format(len(res)))
			print(res)
			#w_csv(res, 'test_report_server.csv')
			self.response_queue.add("Finished Report request " + str(id(self)))
			self.close_con()
			return

		

		#print("Message: ", mess)
		if mess.decode('ascii') == 'exit':

			self._logmsg("Exit instructions received. Shutting down")
			self.response_queue.add("exit")
			self.close_con()
			return
	def _respadd(self, message):
		d_t = datetime.datetime.now(timezone.utc).isoformat()
		if message == "exit":mess = message
		else: mess = d_t + ': '+ str(message)
		
		while self.resp_lock.locked():
			continue
		try:

			self.resp_lock.acquire()
			self.response_queue.add(mess)
		except Exception as E:
			mess = d_t + ': ' + "ERROR: " + str(E)
			print("Problem locking resp")
			self.response_queue.add(mess)
		finally:
			#print("lol")
			if self.resp_lock.locked(): self.resp_lock.release()


	def run(self):
		self.process_message()
		return







