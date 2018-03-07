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


	def tick_update(self):
		# if rn.uniform(0,100) < 0.99**clock.GOAL_FPS:
		# 	self.power -= 1
		# if self.power <= 0:
		# 	self.dead = True

		self.radius += 120*np.sqrt(self.power)/clock.GOAL_FPS
		if self.radius > 50+25*self.power:
			self.dead = True
		else:
			self.collidables[0].radius = self.radius

		


	def draw(self, surface):
		if self.dead:
			return

		c_inner, c_outer = self.colouring()

		r = self.radius
		x = self.position[0]
		y = self.position[1]

		for i in range(int(10 * np.sqrt(self.power))):

			# d = rn.uniform(0,360)
			# gfx.pixel(surface, int(x+r*np.cos(d)), int(y+r*np.sin(d)), 3, c_inner)
			d = rn.uniform(0,2*np.pi)
			gfx.filled_circle(surface, int(x+r*np.cos(d)), int(y+r*np.sin(d)), 3, c_inner)
			gfx.aacircle(surface, int(x+r*np.cos(d)), int(y+r*np.sin(d)), 3, c_outer)
		# gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), int(self.radius)+1, c_outer)
		# gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), int(self.radius), c_inner)
			
