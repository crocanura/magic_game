import numpy as np 
from base_spells import *
import pygame as pg
import pygame.gfxdraw as gfx
import pygame.math as pgmath
import math_tools
import clock
import collidables
import random as rn

class Missile(Base_spell):

	def __init__(self, position=(0,0), direction=0, bounds=[0,0,0,0], power=1, a=0, b=0):
		Base_spell.__init__(self, power, a, b, types[2]['missile'], position)


		self.direction = direction
		self.min_x = bounds[0]
		self.min_y = bounds[1]
		self.max_x = bounds[2]
		self.max_y = bounds[3]
		
		self.port_corner = None
		self.starboard_corner = None
		self.back = self.position + pgmath.Vector2(*math_tools.cartesian_from_polar(10.0+self.power, 180+self.direction))

		self.previous_position = self.back
		self.collidables = [collidables.Collision_segment(self.previous_position, self.position), None, None]

		self.update_fins()

		self.velocity = pgmath.Vector2
		self.update_velocity()


	def update_fins(self):
		vec = pgmath.Vector2(*math_tools.cartesian_from_polar(10.0+self.power, 180+self.direction))
		self.back = self.position + vec
		vec = pgmath.Vector2(*math_tools.cartesian_from_polar(5.0, 90+self.direction))
		self.port_corner = self.back + vec
		self.starboard_corner = self.back - vec

		self.collidables[1] = collidables.Collision_segment(self.position, self.port_corner)
		self.collidables[2] = collidables.Collision_segment(self.position, self.starboard_corner)


	def update_velocity(self):
		self.velocity = pgmath.Vector2(*math_tools.cartesian_from_polar(200+100*self.power, self.direction))


	def tick_update(self):
		if self.status == 'dead':
			return

		self.previous_position = self.position
		self.position = self.position + self.velocity/clock.GOAL_FPS

		self.update_velocity()

		# advance collision segment
		tmp = self.collidables[0].p1
		self.collidables[0].p1 = self.collidables[0].p2
		tmp[0], tmp[1] = self.position[0], self.position[1]
		self.collidables[0].p2 = tmp
		
		self.update_fins()

		self.status = 'dead' # maybe
		for point in [self.position, self.port_corner, self.starboard_corner]:
			if not self.point_out_of_bounds(point):
				self.status = 'alive'


	def point_out_of_bounds(self, point):
		if point[0] < self.min_x or point[0] > self.max_x:
			return True
		if point[1] < self.min_y or point[1] > self.max_y:
			return True
		return False

	def draw(self, surface):
		if self.status == 'dead':
			return

		c_inner, c_outer = self.colouring()

		for i in range(min(self.power, 3)):
			bsc = rn.uniform(0,1)
			b = (self.back - self.position) * bsc
			s = (self.port_corner - self.back) * rn.uniform(-1,1) * bsc
			p = self.back + b + s
			# gfx.filled_circle(surface, int(p[0]), int(p[1]), 3, c_inner)
			gfx.aacircle(surface, int(p[0]), int(p[1]), 3, c_outer)
		# if not c_inner is None:
		gfx.filled_polygon(surface, [self.position, self.port_corner, self.starboard_corner], c_inner)
			# print "drew inner at %s, %s, %s" % (self.position, self.port_corner, self.starboard_corner)
		# if not c_outer is None:
		gfx.aapolygon(surface, [self.position, self.port_corner, self.starboard_corner], c_outer)
			# print "drew outer at %s, %s, %s" % (self.position, self.port_corner, self.starboard_corner)

