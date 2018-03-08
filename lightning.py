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

class Lightning(Base_spell):
	def __init__(self, position, direction, power=1, a=0, b=0):
		Base_spell.__init__(self, power, a, b, types[2]['lightning'], position)

		# self.tree = {self.position}
		self.direction = direction

		d = np.radians(self.direction + rn.uniform(-45, 45))
		l = rn.uniform(25, 100)
		move = pgmath.Vector2(l*np.cos(d), l*np.sin(d))
		next_point = self.position + move

		segment = collidables.Collision_segment(self.position, next_point)

		self.collidables = [segment]
		self.branches = [[segment]]
		# self.tree = { self.position: [next_point] }


	def tick_update(self):
		if self.status == 'dead':
			return

		if self.status == 'dying':
			self.death_animation -= 1
			if self.death_animation <= 0:
				self.status = 'dead'
			return


		current_depth = len(self.branches)
		branch_start = min(rn.randint(0, current_depth * 2), current_depth - 1)
		starting_point = rn.choice([segment.p2 for segment in self.branches[branch_start]])
		# print branch_start
		if branch_start >= 3 + self.power:
			self.status = 'dead'
			self.death_animation = clock.GOAL_FPS / 4
			return
		
		d = np.radians(self.direction + rn.uniform(-45, 45))
		l = rn.uniform(25, 100)
		move = pgmath.Vector2(l*np.cos(d), l*np.sin(d))
		next_point = starting_point + move

		segment = collidables.Collision_segment(starting_point, next_point)
		self.collidables.append(segment)
		if branch_start == len(self.branches) - 1:
			self.branches.append([])

		self.branches[branch_start+1].append(segment)

		# self.tree

	def draw(self, surface):
		if self.status == 'dead':
			return

		c_inner, c_outer = self.colouring()


		for row in self.branches:
			for segment in row:
				sp = segment.p1
				ep = segment.p2
				d, l = (sp - ep).as_polar()
				p1 = sp + 1*np.cos(np.radians(d + 90))
				p2 = sp + 1*np.cos(np.radians(d - 90))
				p3 = ep + 1*np.cos(np.radians(d + 90))
				p4 = ep + 1*np.cos(np.radians(d - 90))
				gfx.aapolygon(surface, [p1, p2, p3, p4], c_outer)
				gfx.filled_polygon(surface, [p1, p2, p3, p4], c_outer)

		for row in self.branches:
			for segment in row:
				sp = segment.p1
				ep = segment.p2
				pdraw.aaline(surface, c_inner, sp, ep, 1)


