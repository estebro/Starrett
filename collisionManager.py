"""
	Responsible for handling all calculations
	and outcomes arising from any collision
	on the board. This class handles both 
	ball-to-wall and ball-to-ball collisions.
"""
import math, time
from ball import Ball


class collisionManager():
	def __init__(self):
		self.ball_collisions = []

	""" determines the post-collision velocities for the
		two balls b1 and b2

		[updates objects' x_vel and y_vel]
	"""
	def ball_to_ball(self, b1, b2):

		normalUnit = self.normalUnit_vct(b1,b2)
		tangentUnit = self.tangentUnit_vct(normalUnit)

		# projecting velocity vectors unto unit normal/tangent vectors
		vn1 = self.dot_product(((b1.x_vel,b1.y_vel),normalUnit))
		vt1 = self.dot_product(((b1.x_vel,b1.y_vel),tangentUnit))
		vn2 = self.dot_product(((b2.x_vel,b2.y_vel),normalUnit))
		vt2 = self.dot_product(((b2.x_vel,b2.y_vel),tangentUnit))
		# tangential velocities (after the collision) remain
		# the same and thus vt1 and vt2 remain unchanged

		# determine normal velocity projections after the collision
		vn1_post, vn2_post = self.post_normal_vel(b1,b2,vn1,vn2)

		# convert scalar normal/tangential velocities into vectors
		b1_vel_vct = self.post_vel_vct(vt1,vn1_post, tangentUnit[0], \
						tangentUnit[1], normalUnit[0], normalUnit[1])
		b2_vel_vct = self.post_vel_vct(vt2,vn2_post, tangentUnit[0], \
						tangentUnit[1], normalUnit[0], normalUnit[1])

		# update x_vel and y_vel of each ball
		b1.set_velocity(b1_vel_vct[0],b1_vel_vct[1])
		b2.set_velocity(b2_vel_vct[0],b2_vel_vct[1])

	""" returns tuple containing normal vector

		input(s):
		b1 		ball number one
		b2 		ball number two
	"""
	def normalUnit_vct(self, b1, b2):
		delta_x = b2.x_pos - b1.x_pos
		delta_y = b2.y_pos - b1.y_pos
		
		if (b1.equals(b2)):
			print 'You gave me the same balls!'

		#time.sleep(5)
		print '\nInside normalUnit_vct()'
		print ('Ball1: ' + str(b1) + ' Ball2: ' + str(b2))
		print ('Delta x/y: ' + str(delta_x) + ' and ' + str(delta_y))
		magnitude = (float)(math.sqrt(delta_x**2 + delta_y**2))
		#time.sleep(5)
		print('Magnitude: ' + str(magnitude))
		try:
			normalUnit_vct = (delta_x / magnitude, delta_y / magnitude)
		except Exception:
			print 'Division by zero.'
			time.sleep(5)	
		return normalUnit_vct

	""" returns tuple containing tangent vector

		input(s):
		*normal 	tuple with x/y components of the normal vector
	"""
	def tangentUnit_vct(self, *normal):
		x,y = normal[0]
		tangentUnit = (-y, x)
		return tangentUnit

	""" returns dot product result (scalar)

		input(s):
		*vcts 		tuple with the two vectors (as tuples) to be operated on 
	"""
	def dot_product(self, *vcts):
		vct1,vct2 = vcts[0]
		vct1_x,vct1_y = vct1
		vct2_x,vct2_y = vct2

		return vct1_x*vct2_x + vct1_y*vct2_y

	""" returns tuple containing the post-collision normal
		velocities of both balls involved
		
		inputs(s):
		b1 		ball number one
		b2 		ball number two
		vn1 	projection of velocity on unit normal vector 1
		vn2 	projection of velocity on unit normal vector 2
	"""
	def post_normal_vel(self, b1, b2, vn1, vn2):
		post_vn1 = vn1 * (b1.mass - b2.mass) + 2 * (b2.mass) * vn2
		post_vn1 /= (b1.mass + b2.mass)

		post_vn2 = vn2 * (b2.mass - b1.mass) + 2 * (b1.mass) * vn1
		post_vn2 /= (b1.mass + b2.mass)

		return (post_vn1, post_vn2)

	""" returns tuple containing the post-collision
		velocities in the x/y coordinate system

		input(s): 
		vt 		projection of velocity on unit tangent vector
		vn 		projection of velocity on unit normal vector
		ut_x 	x-coordinate of unit tangent vector
		ut_y 	y-coordinate of unit tangent vector
		un_x 	x-coordinate of unit normal vector
		un_y 	y-coordinate of unit normal vector
	"""
	def post_vel_vct(self, vt, vn, ut_x, ut_y, un_x, un_y):
		vct_x = vt * ut_x + vn * un_x
		vct_y = vt * ut_y + vn * un_y

		return (vct_x, vct_y)	# tuple containing velocity components

	""" determines whether a collision has occurred between two balls

		input(s):
		b1 		ball number one
		b2 		ball number two
	"""
	def if_ball_collision(self, b1, balls):

		self.ball_collisions = []

		if (len(balls) > 1):	# if list includes other balls

			for b2 in balls:
				if (not (b1.equals(b2))):	# not checking itself

					# determine the next position for both balls
					b1_next_x = b1.x_pos + b1.radius + b1.x_vel
					b2_next_x = b2.x_pos + b2.radius + b2.x_vel
					b1_next_y = b1.y_pos + b1.radius + b1.y_vel
					b2_next_y = b2.y_pos + b2.radius + b2.y_vel
					delta_x = b2_next_x - b1_next_x
					delta_y = b2_next_y - b1_next_y

					# delta_x = (b2.x_pos + b2.radius) - (b1.x_pos + b1.radius)
					# delta_y = (b2.y_pos + b2.radius) - (b1.y_pos + b1.radius)
					
					# distance between the centers of both balls
					distance = (float)(math.sqrt(delta_x**2 + delta_y**2))

					#print 'distance: ' + str(distance) + 'radius1: ' + str(b1.radius) + \
					#	'radius2: ' + str(b2.radius)
					if (distance < b1.radius + b2.radius):
						# print 'distance: '+str(distance)
						# print 'b1: '+str((b1.x_pos,b1.y_pos))
						# print 'b2: '+str((b2.x_pos,b2.y_pos))

						# attach ball to list of collisions
						self.ball_collisions.append(b2)
				else: pass
					# print 'These two %s and %s are equal' % (str(b1),str(b2))

		# print ('List of length: ' + str(len(self.ball_collisions)))
		return self.ball_collisions

	def vel_to_ball(self, b1, b2):

		difference_x = (b2.x_pos + b2.radius) - (b1.x_pos + b1.radius)
		difference_y = (b2.y_pos + b2.radius) - (b1.y_pos + b1.radius)
		# print '\n(' + str(difference_x) + ',' + str(difference_y) + ')'

		# calculate distance so that their edges touch
		dist = float(math.sqrt(difference_x**2 + difference_y**2))
		dist -= (b1.radius + b2.radius)		# distance to be covered

		# used to later determine magnitude of x/y shifts
		angle = math.atan2(b1.y_vel,b1.x_vel)

		# # used to determine how much to move in either x/y directions
		# b1b2_ratio_x = abs( float(b1.x_vel) / (abs(b1.x_vel) + abs(b2.x_vel)) )
		# b1b2_ratio_y = abs( float(b1.y_vel) / (abs(b1.y_vel) + abs(b2.y_vel)) )

		# # calculate the displacement needed for ball 'b1'
		# b1_x_displacement = (dist * b1b2_ratio_x) * math.cos(angle)
		# b1_y_displacement = (dist * b1b2_ratio_y) * math.sin(angle)

		# calculate the displacement needed for ball 'b1'
		b1_x_displacement = (dist) * math.cos(angle)
		b1_y_displacement = (dist) * math.sin(angle)


		# print 'displacements: ' +str(b1_x_displacement)+' '+str(b1_y_displacement)
		return b1_x_displacement, b1_y_displacement


	""" determines whether a collision has occurred between a ball
		and any of the four walls defining the board
	
		input(s):
		b1 		ball number one
		height	height of the board (in pixels)
		width	width of the board (in pixels)
	"""
	def if_wall_collision(self, b1, height, width):
		assert (height > 0 and width > 0), 'Invalid board dimensions.'

		# location of the edges are calculated this way because the 
		# figure is drawn starting at the top left corner
		left_edge = b1.x_pos + b1.x_vel
		right_edge = b1.x_pos + b1.radius * 2 + b1.x_vel
		top_edge = b1.y_pos + b1.y_vel
		bottom_edge = b1.y_pos + b1.radius * 2 + b1.y_vel

		# if any of the ball's edges are located past the
		# locations of the walls, then a collision occurred
		if (left_edge < 0 or right_edge > width):
			return "X_WALL"
		elif (top_edge < 0 or bottom_edge > height):
			return "Y_WALL"
		else:
			return "NONE" 	# false if no collision

	"""	determines the respective x/y velocities needed for 
		an object to just make contact with a wall
	"""
	def vel_to_wall(self, b1, collision_wall, height, width):

		if (collision_wall == "X_WALL"):
			sign = b1.x_vel / abs(b1.x_vel)
			if (b1.x_vel < 0):		# if it was moving left
				to_wall = b1.x_pos
			else:					# if it was moving right
				to_wall = width - (b1.x_pos + 2 * b1.radius)
			vel_ratio = float(to_wall) / abs(b1.x_vel)
			return sign * to_wall, round(vel_ratio * b1.y_vel)
		else:
			sign = b1.y_vel / abs(b1.y_vel)
			if (b1.y_vel < 0):		# if it was moving up
				to_wall = b1.y_pos
			else:					# if it was moving down
				to_wall = height - (b1.y_pos + 2 * b1.radius)
			vel_ratio = float(to_wall) / abs(b1.y_vel)
			return round(vel_ratio * b1.x_vel), sign * to_wall

	""" updates the velocity components of an object to 
		physically represent the velocity after it has 
		experienced a collision with a wall
	"""
	def ball_to_wall(self, b1, collision_wall):
	
		if (collision_wall == 'X_WALL'):
			r_vel = -1 * b1.x_vel	# reflects off x
			b1.set_velocity(r_vel,b1.y_vel)
		else:
			r_vel = -1 * b1.y_vel	# reflects off y
			b1.set_velocity(b1.x_vel,r_vel)

	def sign(self, number):
		return number / abs(number)