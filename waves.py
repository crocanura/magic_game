import numpy as np 
from base_spells import *
import pygame as pg
import pygame.gfxdraw as gfx
import pygame.math as pgmath
import math_tools
import clock
import random as rn
import collidables

class Wave(Base_spell):
	def __init__(self, position, power=1, a=0, b=0):
		Base_spell.__init__(self, power, a, b, types[2]['wave'], position)

		self.radius = 0
		self.collidables = [collidables.Collision_circle(self.position, self.radius)]

		self.direction = None
		self.death_animation = None


	def tick_update(self):
		if self.status == 'dead':
			return
		if self.status == 'dying':
			self.death_animation -= 1
			self.radius = max(0, self.radius - 120*np.sqrt(self.power)/clock.GOAL_FPS)

			# print self.death_animation
			if self.death_animation <= 0:
				self.status = 'dead'
				# print 'killed'
			return

		self.radius += 120*np.sqrt(self.power)/clock.GOAL_FPS
		if self.radius > 50+25*self.power:
			self.status = 'dying'
			self.death_animation = clock.GOAL_FPS / 4
		else:
			self.collidables[0].radius = self.radius

		


	def draw(self, surface):
		if self.status == 'dead':
			return
		elif self.status == 'dying':
			N = int(np.sqrt(self.power) * 10 * 4 * (float(self.death_animation) / clock.GOAL_FPS)**2)
		else:
			N = int(10 * np.sqrt(self.power))

		c_inner, c_outer = self.colouring()

		r = self.radius
		x = self.position[0]
		y = self.position[1]

		for i in range(N):

			# d = rn.uniform(0,360)
			# gfx.pixel(surface, int(x+r*np.cos(d)), int(y+r*np.sin(d)), 3, c_inner)
			if self.direction is None:
				d = rn.uniform(0,360)
			else:
				s = 180 * 4 * (float(self.death_animation) / clock.GOAL_FPS)**2
				d = self.direction + rn.uniform(-s,s)
			gfx.filled_circle(surface, int(x+r*np.cos(np.radians(d))), int(y+r*np.sin(np.radians(d))), 3, c_inner)
			gfx.aacircle(surface, int(x+r*np.cos(np.radians(d))), int(y+r*np.sin(np.radians(d))), 3, c_outer)
		# gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), int(self.radius)+1, c_outer)
		# gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), int(self.radius), c_inner)
			
