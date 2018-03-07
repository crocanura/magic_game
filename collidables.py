import math_tools

class Collidable():
	def __init__(self, type):
		self.type = type

class Collision_point(Collidable):
	def __init__(self, point):
		Collidable.__init__(self, 'point')
		self.location = point

	def check_collision(self, other):
		if other.type == 'point':
			return self.point == other.point
		elif other.type == 'circle':
			return self.point.distance_to(other.center) <= other.radius
		elif other.type == 'segment':
			return math_tools.on_segment(other.p1, self.point, other.p2)
		else:
			return None


class Collision_circle(Collidable):
	def __init__(self, point, radius):
		Collidable.__init__(self, 'circle')
		self.center = point
		self.radius = radius

	def check_collision(self, other):
		if other.type == 'point':
			return self.center.distance_to(other.point) <=  self.radius
		elif other.type == 'circle':
			return self.center.distance_to(other.center) <= self.radius + other.radius
		elif other.type == 'segment':
			return math_tools.segment_hits_circle(other.p1, other.p2, self.center, self.radius)
		else:
			return None

class Collision_segment(Collidable):
	def __init__(self, point1, point2):
		Collidable.__init__(self, 'segment')
		self.p1 = point1
		self.p2 = point2

	def check_collision(self, other):
			if other.type == 'point':
				return math_tools.on_segment(self.p1, other.point, self.p2)
			elif other.type == 'circle':
				return math_tools.segment_hits_circle(self.p1, self.p2, other.center, other.radius)
			elif other.type == 'segment':
				return math_tools.segments_intersect((self.p1, self.p2), (other.p1, other.p2))
			else:
				return None
