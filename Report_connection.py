#report connection
from Serv_connection import *
class Report_connection(Serv_connection):
	def __init__(self, connection):
		super().__init__(connection)
	def receive_rep(self, chunk_size = 1024):
		results = []
		old_msg = bytes()
		while True:
			msg = self.receive(chunk_size)
			msg_len = len(msg)
			if msg_len <= 0: return results
			if msg[msg_len-1:msg_len] == b'\n' and old_msg:
				results += self.process_report_chunk(old_msg + msg)
				old_msg = bytes()
			elif msg[msg_len-1:msg_len] == b'\n' and not old_msg:
				results += self.process_report_chunk(msg)
			else: old_msg += msg
		return results
	def process_report_chunk(self, data, encoding = 'ascii'):
		#@TODO: needs error handling for the decoding
		results = []
		text=  data.decode(encoding).split('\n')
		text_len = len(text)
		#each element should be a list since they represent rows in a spreadsheet/report
		#text_len-1 because split('\n') leaves a single '' at the end of the list
		results = [text[i].split('\t') for i in range(0, text_len-1)]
		#for i in range(0, text_len-1): results.append(text[i])
		return results



