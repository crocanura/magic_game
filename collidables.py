import math_tools

class Collidable():
	def __init__(self, type):
		self.type = type

class Collision_point(Collidable):
	def __init__(self, point):
		Collidable.__init__(self, 'point')
		self.location = point

	def check_collision(self, other, inside_is_correct_place = False):
		if other.type == 'point':
			return self.point == other.point

		elif other.type == 'circle':
			d = self.point.distance_to(other.center)

			if d == other.radius: return True
			elif inside_is_correct_place: return (d > other.radius)
			else: return (d < other.radius)

		elif other.type == 'segment':
			return math_tools.on_segment(other.p1, self.point, other.p2)

		else:
			return None


class Collision_circle(Collidable):
	def __init__(self, point, radius):
		Collidable.__init__(self, 'circle')
		self.center = point
		self.radius = radius

	def check_collision(self, other, inside_is_correct_place = False):
		if other.type == 'point':
			d = other.point.distance_to(self.center)

			if d == self.radius: return True
			elif inside_is_correct_place: return (d > self.radius)
			else: return (d < self.radius)

		elif other.type == 'circle':
			if math_tools.circles_far(self.center, self.radius, other.center, other.radius):
				if inside_is_correct_place:
					return True
				else: return False

			elif math_tools.circle_enveloped_by_circle(self.center, self.radius, other.center, other.radius):
				if inside_is_correct_place: return False
				else: return True

			elif math_tools.circle_enveloped_by_circle(other.center, other.radius, self.center, self.radius):
				if inside_is_correct_place: return False
				else: return True

			else: return True

		elif other.type == 'segment':
			if math_tools.segment_hits_circle(other.p1, other.p2, self.center, self.radius):
				return True

			elif math_tools.segment_enveloped_by_circle(other.p1, other.p2, self.center, self.radius):
				if inside_is_correct_place: return False
				else: return True

			else: return inside_is_correct_place

		else: return None

class Collision_segment(Collidable):
	def __init__(self, point1, point2):
		Collidable.__init__(self, 'segment')
		self.p1 = point1
		self.p2 = point2

	def check_collision(self, other, inside_is_correct_place = False):
		if other.type == 'point':
			return math_tools.on_segment(other.p1, self.point, other.p2)

		elif other.type == 'circle':
			if math_tools.segment_hits_circle(self.p1, self.p2, other.center, other.radius):
				return True

			elif math_tools.segment_enveloped_by_circle(self.p1, self.p2, other.center, other.radius):
				if inside_is_correct_place: return False
				else: return True

			else: return inside_is_correct_place

		elif other.type == 'segment':
			return math_tools.segments_intersect((self.p1, self.p2), (other.p1, other.p2))

		else:
			return None
