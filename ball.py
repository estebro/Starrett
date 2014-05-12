"""
	Represents a circle found in the board
	and contains all of its attributes
	including location, radius, and mass.
"""

from PySide.QtGui import (QGraphicsEllipseItem)

class Ball(QGraphicsEllipseItem):
	def __init__(self, x_pos, y_pos, mass, radius):
		super(Ball,self).__init__(x_pos,y_pos,2*radius,2*radius)
		self.x_pos = x_pos
		self.x_start = x_pos
		self.y_pos = y_pos
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

	def __str__(self):
		return 'Ball at ('+str(self.x_pos)+','+str(self.y_pos)+') with velocity ' + \
					str(self.x_vel)+' .x. + '+str(self.y_vel)+' .y.'