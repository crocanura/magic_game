import time

GOAL_FPS = 120
tick_time = 1.0/GOAL_FPS

last_tick = time.time()


def next_tick():
	"""Moves the game to the next tick, does nothing meanwhile"""

	global last_tick

	a = time.time()
	counter = 0

	# print "clock: %2.2f%% of a tick to spare" % (100*(last_tick + tick_time - a)/tick_time)

	while a < last_tick + tick_time:
		# time.sleep(tick_time/10.0)
		a = time.time()
		counter += 1
	last_tick = a