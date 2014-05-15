import socket, threading, Queue, select

from server_broadcast import BroadcastThread
from server_client import ServeClientThread


"""
	Responsible for handling the setup of client/server
	connections via TCP.

"""
class ServerThread(threading.Thread):

	def __init__(self, tcp_queue, event):
		threading.Thread.__init__(self)
		self.host = '127.0.0.1'
		self.port = 3333
		self.tcp_main_queue = tcp_queue
		self.client_queue = Queue.Queue()
		self.thread_event = event
		self.manager = BroadcastThread(tcp_queue)
		self.manager.start()

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
			clients_read, wlist, xlist = select.select([self.tcpsocket],[],[],2)
			for client in clients_read:
				
				# retrieve ip and port from client socket
				(clientsock, (ip,port)) = client.accept()
				
				print 'Made it here'
				# initiate client thread on server
				newthread = ServeClientThread(ip,port,clientsock,self.client_queue)
				newthread.daemon = True
				newthread.start()
				print '[+] New thread started for '+str(ip)+':'+str(port)
				
				# add client thread to the broadcast manager
				self.manager.addClientThread(newthread)
				print '\nListening for incoming connections...'
			

	# sends data to all tcp clients
	def broadcast(self,msg):
		for t in self.threads:
			t.socket.send(msg)

	# returns the name of the thread
	def __str__(self):
		return 'SERVER'