import socket, threading

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
		data = self.socket.recv(2048)

		try:
			while (data != ''):
				print 'Client sent: '+data+' size: '+str(len(data))
				self.socket.send('You sent me:'+data)
				data = self.socket.recv(2048)
		except Exception:
			print 'Client disconnected...'
			self.socket.close()

class ServerThread(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.port = 3333

	def run(self):
		self.tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		self.tcpsocket.bind((self.host,self.port))
		self.threads = []

		while True:
			self.tcpsocket.listen(4)
			print '\nListening for incoming connections...'
			(clientsock, (ip,retPort)) = self.tcpsocket.accept()
			newthread = ServeClientThread(ip,retPort,clientsock)
			newthread.start()
			self.threads.append(newthread)

		for t in self.threads:
			t.join()

	def broadcast(self,msg):
		for t in self.threads:
			t.socket.send(msg)