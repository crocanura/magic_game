import pygame.math as pgmath

class Game_object(object):

	def __init__(self, position):
		self.position = pgmath.Vector2(position)
		self.collidables = []

		self.status = 'living'
		self.death_animation = None # number indicating progress through death animation
		self.silenced = False

		self.checked_collisions = {} # this must be reset before collision checking

	
	def check_collision(self, other):
		inside_is_correct_place = False

		val = False

		for c1 in self.collidables:
			for c2 in other.collidables:
				if hasattr(self, 'should_contain'):
					if other in self.should_contain:
						inside_is_correct_place = True
				if hasattr(other, 'should_contain'):
					if self in other.should_contain:
						inside_is_correct_place = True
				
				if c1.check_collision(c2, inside_is_correct_place):
					val = True
					break
			if val: break

		self.checked_collisions[other] = val
		other.checked_collisions[self] = val

		# print "Checked collision between G.O. %s and G.O. %s" % (self, other)
		# print "Determined collision %s" % val

		return val


	def kill(self):
		self.status = 'dead'


	def silence(self):
		self.silenced = True