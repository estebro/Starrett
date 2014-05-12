import time, socket, threading

class ClientThread(threading.Thread):

	def __init__(self, data, main_queue, sim_queue):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.port = 3333
		self.data_send = data
		self.data_recv = ''
		self.tcp_main_queue = main_queue
		self.tcp_sim_queue = sim_queue

		# setting up the socket (non-blocking)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.host,self.port))
		self.s.setblocking(0)

	# send data via existing tcp socket
	def sendUpdate(self, data):
		self.data_send = data
		self.s.send(self.data_send)	# send data

	# receive data via existing tcp socket
	def checkForUpdate(self):
		self.data_recv = self.s.recv(1024)
		return self.data_recv

	# close existing tcp socket
	def closeConnection(self):
		self.s.close()

	# parses values into a string to be sent via tcp
	def encode(self,x,y,xv,yv,m,r):
		msg = 'x'+str(x)+'y'+str(y)+'xv'+str(xv)+'yv'+str(yv)+'m'+str(m)+'r'+str(r)
		return msg

	def run(self):
		
		while True:
			try:
				self.checkForUpdate()	# retrieve data from server
				print ('Received scenario update: ' + self.data_recv)
				if (self.data_recv != 'Welcome to the server.'):
					# pass this to thread handling physics
					self.tcp_sim_queue.put(self.data_recv)
			except Exception:
				if (not self.tcp_main_queue.empty()):
					# retrieves input from thread queue
					self.data_send = self.tcp_main_queue.get()	# waits if none
					print 'Data sent @ tcp_client: ' + self.data_send
					self.sendUpdate(self.data_send)	# to server

								

if __name__ == '__main__':
	client = ClientThread()
	print('Server welcome: '+client.checkForUpdate())
	data = [5,9,20,3]
	time.sleep(10)
	print('Server says: '+client.checkForUpdate())
	client.closeConnection()