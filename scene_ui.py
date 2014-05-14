"""
	Responsible for setting up the QGraphicsScene which populates
	the QGraphicsView used to display the animation of all 
	objects simulated in the program.

"""

from PySide.QtGui import (QGraphicsScene)
from ball import Ball
from collisionManager import collisionManager

# graphicsView dimensions
SCENE_WIDTH = 579
SCENE_HEIGHT = 309

class SceneManager():
	
	def __init__(self, graphicsView, queue):
		self.scene = QGraphicsScene()
		self.scene.setSceneRect(0,0,SCENE_WIDTH,SCENE_HEIGHT)
		graphicsView.setScene(self.scene)

		# handles physics involved in collisiions/detection
		self.cm = collisionManager()
		self.sim_queue = queue  # to receive data from threads

	# add object to simulation scene (given parameters)
	# input:	'values'  contains (x,y,x_vel,y_vel,mass,radius)
	def addItem(self,param):
		values = self.decode(param)
		item = Ball(values[0],values[1],values[4],values[5])
		item.set_velocity(values[2],values[3])
		self.scene.addItem(item)

	# translate parameters received by TCP
	def decode(self,msg):
		delims = ['r','m','yv','xv','y','x']
		values = []

		# traverses delimeters to extract values
		for i in range(len(delims)):
			index = msg.index(delims[i])			# search for delimeter
			arg = msg[index + len(delims[i]) :]		# extract value
			values.append(int(arg))					# store value
			msg = msg[:index]				# reduce message left to parse
		
		values.reverse()
		return values

	# access all items in the simulation scene
	def getItems(self):
		return self.scene.items()

	# determine an item's next location
	def next_move(self,item):
		
		# check whether any ball-to-ball collisions will occur
		collisions = self.cm.if_ball_collision(item,self.getItems())
		
		if (len(collisions) > 0):	# colllision identified
			print '\nInside next_move()'
			print ('Item: ' + str(item) + ' List: ' )#+ str(collisions))
			for ball in collisions:
				print str(ball)
			# obtain velocities so that balls just collide
			delta_x, delta_y = self.cm.vel_to_ball(item,collisions[0])
			# delta_x = item.x_vel
			# delta_y = item.y_vel
			self.cm.ball_to_ball(item,collisions[0])
		else:
			# determine if a wall will be hit in the next move
			hit_wall = self.cm.if_wall_collision(item,SCENE_HEIGHT,SCENE_WIDTH)

			if (hit_wall != 'NONE'):	# if wall collision will occur
				# determine displacement left to collide with wall
				delta_x, delta_y = self.cm.vel_to_wall(item,hit_wall,SCENE_HEIGHT,SCENE_WIDTH)
				# set object's velocity after impacting the wall
				self.cm.ball_to_wall(item,hit_wall)
			else:
				#keep the ball in the same trajectory
				delta_x = item.x_vel
				delta_y = item.y_vel

		# next x/y destination of the item in LOCAL coordinates
        # require the offsets (-item.x_start and -item.y_start)
        # given the fact that the item.x_pos and item.y_pos values
        # represent locations in global coordinates
		next_x = item.x_pos + delta_x - item.x_start
		next_y = item.y_pos + delta_y - item.y_start

		return next_x,next_y