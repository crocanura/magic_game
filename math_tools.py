import numpy as np
import pygame.math as pgmath


def cartesian_from_polar(r, theta):
	return (r*np.cos(np.radians(theta)), r*np.sin(np.radians(theta)))



## These two functions adapted from online
## See https://www.geeksforgeeks.org/orientation-3-ordered-points/
## for details
def on_segment(p, q, r):
	if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]):
		if q[1] <= max(p[1], r[1]) and q[1] >= min(p[1], r[1]):
			return True
 
	return False

def orientation(p, q, r):

	val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
 
	if (val == 0):
		return 0
 
	elif val > 0:
		return 1

	return 2


def segments_intersect(v_1, v_2):
	p1 = v_1[0]
	p2 = v_2[0]
	q1 = v_1[1]
	q2 = v_2[1]

	o1 = orientation(p1, q1, p2)
	o2 = orientation(p1, q1, q2)
	o3 = orientation(p2, q2, p1)
	o4 = orientation(p2, q2, q1)
 
	
	if o1 != o2 and o3 != o4:
		return True
 
	## Special Cases
	## p1, q1 and p2 are colinear and p2 lies on segment p1q1
	if (o1 == 0 and on_segment(p1, p2, q1)): return True
 
	## p1, q1 and q2 are colinear and q2 lies on segment p1q1
	if (o2 == 0 and on_segment(p1, q2, q1)): return True
 
	## p2, q2 and p1 are colinear and p1 lies on segment p2q2
	if (o3 == 0 and on_segment(p2, p1, q2)): return True
 
	## p2, q2 and q1 are colinear and q1 lies on segment p2q2
	if (o4 == 0 and on_segment(p2, q1, q2)): return True
 
	return False ## Doesn't fall in any of the above cases





## a onto b
def projection(a, b):
	"""a projected onto b"""
	if a.length() == 0 or b.length() == 0:
		return pgmath.Vector2(0,0)

	return b*(b.dot(a))/(b.length()**2)

def segment_hits_circle(a, b, c, r):
	if a.distance_to(c) <= r or b.distance_to(c) <= r:
		return True

	vec = c - a
	to_d = projection(vec, b-a)
	d = a + to_d

	if d.distance_to(c) <= r:
		return True

	return False