import threading, pickle

"""
	Responsible for updating client applications with the 
	latest simulation results.

"""
class BroadcastThread(threading.Thread):

	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.daemon = True
		self.simulation_queue = queue
		self.threads = []

	# thread's 'main' function
	def run(self):

		while True:
			# if any clients are connected
			if (len(self.threads) > 0):
				# if there's a message on queue
				if (not self.simulation_queue.empty()):
					item = self.simulation_queue.get()	# retrieve message
					serialized = pickle.dumps(item)
					self.updateSimulation(serialized)
					print ('Broadcast: ' + str(item))		#DEBUG


	# stores new thread serving client
	def addClientThread(self, thread):
		self.threads.append(thread)

	# pushes simulation updates to all threads
	def updateSimulation(self, update):
		for client in self.threads:
			try:
				# send update to client
				client.socket.send(update)
			except Exception:
				# remove the thread
				self.threads.remove(client)
				print 'Thread for client <%i> ended.' % client.port