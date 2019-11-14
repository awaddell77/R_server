import socket
from Report_connection import *
from w_csv import *




def start_server(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	
	return sock

def server_listen(sock, listen_queue = 5):
	while True:
		try:
			sock.listen(listen_queue)
			conn, addr = sock.accept()
			print("Connected to: {0}".format(addr))
			print(type(conn))
			print(isinstance(conn, socket.socket))
			c_inst = Report_connection(conn)
			mess = c_inst.receive()
			f_line = mess.find(b'\n')

			if mess[:f_line] == b'report': 
				c_inst.send('hi', 'ascii')
				print("Report Order received")
				res = c_inst.receive_rep()
				
				print("Returned {0} rows".format(len(res)))
				print(res)
				w_csv(res, 'test_report_server.csv')

			

			print("Message: ", mess)
			if mess.decode('ascii') == 'exit':
				print("Exit instructions received. Shutting down")
				c_inst.close()
				return
		except KeyboardInterrupt as KE:
			c_inst.close()
			break

port = 12344
host ='127.0.0.1'
sock = start_server(host, port)
server_listen(sock)
sock.close()