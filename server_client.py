import threading

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
		

	# thread's 'main' function
	def run(self):
		print 'Connection from: '+str(self.ip)+':'+str(self.port)

		self.socket.send('Welcome to the server.')
		# data = 'START'
		
		# while True:		# loop while socket is alive
		# 	try:
		# 		while (data != ''):			# wait for data from client
		# 			if (data != 'START'):	# check for starting condition
		# 				print 'Client ('+str(self.port)+') sent: '+data+'.'
		# 				self.server_queue.put(data)		# pass data to server main thread
		# 			data = self.socket.recv(2048)	# read more data
		# 	except Exception:	# handle broken connection
		# 		print 'Client ('+str(self.port)+') disconnected.'
		# 		self.socket.close()		# properly close socket
		# 		break 		# exit wait-loop