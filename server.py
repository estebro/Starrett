import socket, threading, Queue, select

"""
	Responsible for handling all client/server interaction
	on the server side once connection is established.
"""
class ServeClientThread(threading.Thread):

	def __init__(self,ip,port,socket,queue):
		threading.Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.socket = socket
		self.server_queue = queue
		print '[+] New thread started for '+str(ip)+':'+str(port)

	def run(self):
		print 'Connection from: '+str(self.ip)+':'+str(self.port)

		self.socket.send('Welcome to the server.')
		data = 'START'
		
		while True:		# loop while socket is alive
			try:
				while (data != ''):			# wait for data from client
					if (data != 'START'):	# check for starting condition
						print 'Client ('+str(self.port)+') sent: '+data+'.'
						self.server_queue.put(data)		# pass data to server main thread
					data = self.socket.recv(2048)	# read more data
			except Exception:	# handle broken connection
				print 'Client ('+str(self.port)+') disconnected.'
				self.socket.close()		# properly close socket
				break 		# exit wait-loop


"""
	Responsible for handling the setup of client/server
	connections via TCP.
"""
class ServerThread(threading.Thread):

	def __init__(self, tcp_queue, sim_queue, event):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.port = 3333
		self.tcp_main_queue = tcp_queue
		self.tcp_sim_queue = sim_queue
		self.client_queue = Queue.Queue()
		self.thread_event = event

	def run(self):
		# creating a socket on which server responds
		self.tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.tcpsocket.bind((self.host,self.port))
		self.tcpsocket.listen(4)
		self.threads = []

		print '\nListening for incoming connections...'
		while (not self.thread_event.is_set()):

			# scan for sockets ready to be read (with 1 sec timeout)
			clients_read, wlist, xlist = select.select([self.tcpsocket],[],[],1)
			for client in clients_read:
				
				# retrieve ip and port from client socket
				(clientsock, (ip,retPort)) = client.accept()
				
				# initiate client thread on server
				newthread = ServeClientThread(ip,retPort,clientsock,self.client_queue)
				newthread.daemon = True
				newthread.start()
				self.threads.append(newthread)
				print '\nListening for incoming connections...'
			
			# check for messages from main_gui thread
			if (not self.tcp_main_queue.empty()):
				# if message, broadcast to all client threads
				item = self.tcp_main_queue.get()
				self.broadcast(item)
				self.tcp_sim_queue.put(item)
				print ('Broadcast: ' + item)
			elif (not self.client_queue.empty()):
				item = self.client_queue.get()
				self.tcp_sim_queue.put(item)
				self.broadcast(item)
		

	# sends data to all tcp clients
	def broadcast(self,msg):
		for t in self.threads:
			t.socket.send(msg)