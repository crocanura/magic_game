from common import *
from collections import deque


class ex_collider(object):
	def __init__(self, l):
		self.l = l
		self.checked_collisions = []

	def check_collision(self, obj):
		# print "Collision between %s and %s checked" % (self, obj)
		for item in self.l:
			if item in obj.l:
				return True
		return False

	def __str__(self):
		return "ex_colllider: %s" % str(self.l)

	def __repr__(self):
		return str(self)

# class Collision_collection(object):
# 	def __init__(self):
# 		self.collisions = []

# 		self.blobs = []

def reset_collisions(objs):
	for obj in objs:
		obj.checked_collisions = {}

def collision_blobs(objs):
	remaining =  deque(objs)
	stack = deque()
	blobs = []

	while remaining: # while there are unchecked elements
		stack.append(remaining.pop())
		blob = set()
		while stack: # dfs through touching elements
			item1 = stack.pop()
			to_skip = set()
			for item2 in remaining:
				if item2 in item1.checked_collisions:
					if item1.checked_collisions[item2] == True:
						blob.add(item1)
						blob.add(item2)
						stack.append(item2)
						to_skip.add(item2)
					else:
						continue

				# print "checking %s and %s for collision" % (item1, item2)
				elif item1.check_collision(item2):
					# print "yes collision"
					blob.add(item1)
					blob.add(item2)
					stack.append(item2)
					to_skip.add(item2)
					
			for item2 in to_skip:
				remaining.remove(item2)
				# if item2 in stack:
				# 	stack.remove(item2)
		if blob != empty:
			blobs.append(list(blob))

	return blobs


# a = ex_collider([1, 3])

# b = ex_collider([2, 8])

# c = ex_collider([3, 1, 4, 5, 7])

# d = ex_collider([4, 3, 7])

# e = ex_collider([5, 3, 7])

# f = ex_collider([6])

# g = ex_collider([7, 5, 4])

# h = ex_collider([8, 2])

# objs = [a,b,c,d,e,f,g,h]

# for x in range(2):
# 	objs.extend(objs)

# import time

# st = time.time()
# cb = collision_blobs(objs)
# ed = time.time()
# tot = ed - st