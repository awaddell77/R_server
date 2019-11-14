import socket
from r_csv import *
host = '127.0.0.1'
port = 12344

def connect(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host, port))
	sock.settimeout(10.0)
	#sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	return sock
def write_msg(sock, message, encoding='ascii'):
	sock.send(bytes(message, encoding))
	return
def send_report(sock, fname):
	data = r_csv(fname)
	column_delim = '\t'
	sock.send(bytes("report\n", 'ascii'))
	resp = sock.recv(2)
	if not resp: 
		print("FAILED")
		return
	for i in range(0, len(data)):

		temp = column_delim.join(data[i]) + "\n"
		print("Sending:", temp)
		sock.send(bytes(temp, 'ascii'))
	sock.close()



def end_serv():
	sock = connect(host, port)
	write_msg(sock, 'exit')

try:
	sock = connect(host, port)
	sock2 = connect(host, port)
	#end_serv()
	send_report(sock, 'test_report.csv')
	send_report(sock2, 'test_report.csv')
	#sock.close()
	#write_msg(sock, 'exit')
	#sock.close()
except Exception as E:
	sock.close()
	sock2.close()
	end_serv()