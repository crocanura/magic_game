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


class Charge(Base_spell):
	def __init__(self, position, power=1, a=0, b=0):
		Base_spell.__init__(self, power, a, b, types[2]['charge'], position)

		self.radius = 3+power

		self.collidables = [collidables.Collision_circle(self.position, self.radius)]

		self.ticks = 0
		m = np.sqrt(power)
		self.arm_data = [(rn.uniform(0, 360), rn.uniform(0,360), rn.uniform(m/4.0,m/6.0), rn.uniform(m/4.0,m/6.0), rn.uniform(m/30.0,m/60.0)) for i in range(power)]
		# arm tuple: (polar_phase, radial_phase, polar_frequency, radial_frequency, polar_overcycle_frequency)
		self.arms = [collidables.Collision_segment(self.position, self.position) for i in range(power)]
		# self.collidables.extend(self.arms)
		self.arm_update()


	def arm_update(self):
		if self.status == 'dead':
			return 

		self.radius = 3+self.power
		self.collidables[0].radius = self.radius

		for i in range(len(self.arms)):
			pp, rp, pf, rf, pof = self.arm_data[i]
			t = self.ticks / float(clock.GOAL_FPS)

			overcycle_angle = pof * 360 * t
			p_angle = pp + pf * 360 * np.sin(np.radians(overcycle_angle))
			r_angle = rp + rf * 360 * t
			l = self.radius + 3 + 3 * np.sin(np.radians(r_angle)) # length
			arm_vec = pgmath.Vector2(math_tools.cartesian_from_polar(l, p_angle))
			self.arms[i].p2 = self.position + arm_vec

	def tick_update(self):
		if self.status == 'dead:':
			return

		self.ticks += 1

		self.arm_update()

		if self.ticks > self.power * clock.GOAL_FPS * 5:
			self.status = 'dead'



	def draw(self, surface):
		c_inner, c_outer = self.colouring()

		for arm in self.arms:
			pdraw.aaline(surface, c_outer, arm.p1, arm.p2, 1)

		gfx.filled_circle(surface, int(self.position[0]), int(self.position[1]), self.radius, c_inner)
		gfx.aacircle(surface, int(self.position[0]), int(self.position[1]), self.radius, c_outer)

