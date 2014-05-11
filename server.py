import socket, threading, Queue, select

class ServeClientThread(threading.Thread):

	def __init__(self,ip,port,socket):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		print '[+] New thread started for '+str(ip)+':'+str(port)

	def run(self):
		print 'Connection from: '+str(self.ip)+':'+str(self.port)

		self.socket.send('Welcome to the server.')
		data = ''
		
		while True:		# loop while socket is alive
			try:
				while (data != ''):		# wait for data from client
					print 'Client ('+str(self.port)+') sent: '+data+' size: '+str(len(data))
					self.socket.send('You sent me:'+data)
					data = self.socket.recv(2048)
			except Exception:	# handle broken connection
				print 'Client disconnected.'
				self.socket.close()		# properly close socket
				break 		# exit wait-loop


class ServerThread(threading.Thread):

	def __init__(self, thread_queue):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.port = 3333
		self.queue = thread_queue

	def run(self):
		# creating a socket on which server responds
		self.tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.tcpsocket.bind((self.host,self.port))
		self.tcpsocket.listen(4)
		self.threads = []

		print '\nListening for incoming connections...'
		while True:

			# scan for sockets ready to be read (with 1 sec timeout)
			clients_read, wlist, xlist = select.select([self.tcpsocket],[],[],1)
			for client in clients_read:
				
				# retrieve ip and port from client socket
				(clientsock, (ip,retPort)) = client.accept()
				
				# initiate client thread on server
				newthread = ServeClientThread(ip,retPort,clientsock)
				newthread.start()
				self.threads.append(newthread)
				print '\nListening for incomming connections...'
			
			# check for messages from main_gui thread
			if (not self.queue.empty()):
				# if message, broadcast to all client threads
				self.broadcast(self.queue.get())
			
			print ('Number of threads: ' + str(len(self.threads)))
		
		for t in self.threads:
			t.join()

	def broadcast(self,msg):
		for t in self.threads:
			t.socket.send(msg)