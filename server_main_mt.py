import socket
from R_connection import *
from w_csv import *
import threading
import queue



def start_server(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	
	return sock
log_lst = []
def server_listen(sock, listen_queue = 5):
	response_queue = set()
	lst_lock = threading.Lock()
	resp_lock = threading.Lock()
	thread_lst = []
	thrd_lst = []
	while True:
		print(response_queue)
		if 'exit' in response_queue: 
			alive = [thr.is_alive() for thr in thrd_lst]
			print("ALAAAAAAAAAAN")
			return alive
		try:
			sock.listen(listen_queue)

			conn, addr = sock.accept()
			#c_inst = Report_connection(conn, response_queue)
			#print("Connected to: {0}".format(addr))
			#print(type(conn))
			#print(isinstance(conn, socket.socket))
			thrd_lst.append(R_connection(conn, response_queue, log_lst, lst_lock, resp_lock))
			#R_connection(conn, response_queue, log_lst, lst_lock).start()
			
			thrd_lst[-1].start()
			#if 'exit' in response_queue: return
		except KeyboardInterrupt as KE:
			
			break
		finally:
			print(response_queue)
			if 'exit' in response_queue:
				alive = [thr.is_alive() for thr in thrd_lst]
				return alive

port = 12344
host ='127.0.0.1'
sock = start_server(host, port)
alive = server_listen(sock)
sock.close()
print(log_lst)
print(alive)