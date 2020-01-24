import queue, time, threading, socket
from R_connection import *
from w_csv import *




def start_server(host, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((host, port))
	
	return sock

def modify_locked_var(lock_var, targ_obj, func):
	#obviously has the potential to hang a lot of stuff
	#if called by the main thread too many times
	while lock_var.locked():
		continue
	try:

		lock_var.acquire()
		func(targ_obj)
	except Exception as E:
		mess = d_t + ': ' + "ERROR: " + str(E)
		print("Problem locking")
		#@TODO: Needs to write the server logfile
		#log_info.append(mess)
	finally:
		#print("lol")
		if lock_var.locked(): lock_var.release()

def write_to_servlog(log_lst):
	with open('servlog.txt', 'a') as sfile:
		for i in range(0, len(log_lst)): sfile.writelines(log_lst[i] + '\n')
def dump_log_lst(log_lst):
	write_to_servlog(log_lst)
	print(log_lst) #for testing only
	log_lst.clear()

def log_msg(session_id, mess,connection_id = ''):
	d_t = datetime.datetime.now(timezone.utc).isoformat()
	if connection_id: message = d_t + ' ['+ str(session_id) + '~Connection #' + str(connection_id) + ']: '+ str(mess)
	else: message= d_t + ' ['+ str(session_id) + ']'+ str(mess)
	return message
def server_listen(sock, listen_queue = 5):
	response_queue = set()
	lst_lock = threading.Lock()
	resp_lock = threading.Lock()
	thread_lst = []
	thrd_lst = []
	log_lst = []
	start = time.time()
	session_id = str(round(start))
	connection_id = 1
	while True:
		print(response_queue)
		try:
			sock.listen(listen_queue)
			thrd_lst.append(R_connection(sock.accept(), response_queue, log_lst, lst_lock, resp_lock, 
				connection_id = connection_id, session_id = session_id))
			connection_id += 1
			#R_connection(conn, response_queue, log_lst, lst_lock).start()
			
			thrd_lst[-1].start()
			#if 'exit' in response_queue: return
		except KeyboardInterrupt as KE:
			
			break
		except Exception as E:
			sock.close()
			temp = "Fatal Error Occured: " + str(E)
			while lst_lock.locked():
				print("lst_lock is still locked") 
				continue
			log_lst.append(log_msg(session_id, temp))
			dump_log_lst(log_lst)
			return alive,log_lst


		finally:
			print(response_queue)
			if len(log_lst) >= 2:
				modify_locked_var(lst_lock, log_lst, dump_log_lst)
			if 'exit' in response_queue:
				alive = [thr.is_alive() for thr in thrd_lst]
				print(log_lst)
				modify_locked_var(lst_lock, log_lst, dump_log_lst)

				return alive, log_lst


port = 12344
host ='127.0.0.1'
sock = start_server(host, port)
res = server_listen(sock)
sock.close()
print(res[1]) #log_lst
print(res[0]) #alive