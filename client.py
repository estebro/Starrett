import time, socket, threading, pickle

class ClientThread(threading.Thread):

	def __init__(self, sim_queue, event):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.port = 3333
		self.data_recv = ''
		self.tcp_sim_queue = sim_queue
		self.thread_event = event

		# setting up the socket (non-blocking)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.host,self.port))
		self.s.setblocking(1)


	def run(self):
		
		print 'Success. SERVER: %s' % (self.s.recv(2048))	# server welcome

		while (not self.thread_event.is_set()):
			try:
				tcp_received = self.s.recv(2048)		# data received via tcp
				obj_list = pickle.loads(tcp_received)	# unserialize data

				# print 'Unloaded: %s' % obj_list 	#DEBUG

				# pass simulation data from server to GUI thread
				self.tcp_sim_queue.put(obj_list)
			except Exception:
				print 'Socket error occurred.'
				break

		# returns name of thread
		def __str__(self):
			return 'CLIENT'

if __name__ == '__main__':
	client = ClientThread()
	print('Server welcome: '+client.checkForUpdate())
	data = [5,9,20,3]
	time.sleep(10)
	print('Server says: '+client.checkForUpdate())
	client.closeConnection()