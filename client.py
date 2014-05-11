import time, socket, threading, Queue

class ClientThread(threading.Thread):

	def __init__(self, data, thread_queue):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.port = 3333
		self.data_send = data
		self.data_recv = ''
		self.queue = thread_queue

		#  setting up the socket (non-blocking)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.host,self.port))
		self.s.setblocking(0)

	def sendUpdate(self, data):
		self.data_send = data
		self.s.send(self.data_send)	# send data

	def checkForUpdate(self):
		self.data_recv = self.s.recv(1024)
		return self.data_recv

	def closeConnection(self):
		self.s.close()

	def encode(self,x,y,xv,yv,m,r):
		msg = 'x'+str(x)+'y'+str(y)+'xv'+str(xv)+'yv'+str(yv)+'m'+str(m)+'r'+str(r)
		return msg

	def run(self):
		
		#print self.checkForUpdate()		# print welcome message
		while True:

			try:
				self.checkForUpdate()
				print 'Received scenario update: ' + self.data_recv
					# pass this to thread handling physics
			#while (self.checkForUpdate() == ""):
			except Exception:
				if (not self.queue.empty()):
					# retrieves input from thread queue
					self.data_send = self.queue.get()	# waits if none
					print 'Data sent @ tcp_client: ' + self.data_send
					self.sendUpdate(self.data_send)	# to server

								

if __name__ == '__main__':
	client = ClientThread()
	print('Server welcome: '+client.checkForUpdate())
	data = [5,9,20,3]
	time.sleep(10)
	print('Server says: '+client.checkForUpdate())
	client.closeConnection()