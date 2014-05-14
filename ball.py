"""
	Represents a circle found in the board
	and contains all of its attributes
	including location, radius, and mass.
"""

from PySide.QtGui import (QGraphicsEllipseItem)

class Ball(QGraphicsEllipseItem):
	def __init__(self, x_pos, y_pos, mass, radius):
		super(Ball,self).__init__(x_pos,y_pos,2*radius,2*radius)
		
		# object's current position (global coordinates)
		self.x_pos = x_pos
		self.y_pos = y_pos

		# object's starting position (global coordinates)
		self.x_start = x_pos
		self.y_start = y_pos

		self.radius = radius
		self.mass = mass

		# used in ball collision handling
		self.checked = False

		# ball is originally stationary 
		self.x_vel = 0
		self.y_vel = 0

	def set_location(self, x_pos, y_pos):
		self.x_pos = x_pos
		self.y_pos = y_pos

	def set_velocity(self, x_vel, y_vel):
		self.x_vel = x_vel
		self.y_vel = y_vel

	def equals(self, ball):
		
		if((self.x_pos == ball.x_pos) and (self.y_pos == ball.y_pos)):
			if((self.x_vel == ball.x_vel) and (self.y_vel == ball.y_vel)):
				if((self.radius == ball.radius) and (self.mass == ball.mass)):
					return True

		return False

	def __str__(self):
		return 'x' + str(self.x_pos) + 'y' + str(self.y_pos) + 'xv' + str(self.x_vel) + \
				'yv' + str(self.y_vel) + 'm' + str(self.mass) + 'r' + str(self.radius)