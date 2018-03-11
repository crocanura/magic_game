import numpy as np 
from base_spells import *
import pygame as pg
import pygame.gfxdraw as gfx
import pygame.draw as pdraw
import pygame.math as pgmath
import math_tools
import clock
import collidables
import random as rn


class Pulse(Base_spell):
	def __init__(self, position=(0,0), direction=0, power=1, a=0, b=0):
		
		self.radius = 25 + 10 * power
		vec = pgmath.Vector2(*math_tools.cartesian_from_polar(self.radius, direction))
		Base_spell.__init__(self, power, a, b, types[2]['pulse'], position + vec)

		self.collidables = [collidables.Collision_circle(self.position, self.radius)]

		self.tick_elapsed = False


	def tick_update(self):
		if self.status == 'dead:':
			return
		elif self.status == 'living':
			if self.tick_elapsed:
				self.kill()
			else:
				self.tick_elapsed = True
		

		if self.status == 'dying':
			self.death_animation -= 1.0/clock.GOAL_FPS
			if self.death_animation <= 0:
				self.status = 'dead'


	def kill(self):
		self.death_animation = 0.100
		self.status = 'dying'


	def draw(self, surface):
		if self.status == 'dead':
			return

		c_inner, c_outer = self.colouring()
		gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), self.radius-1, c_outer)
		gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), self.radius, c_inner)
		gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), self.radius+1, c_outer)

