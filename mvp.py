import sys, pygame, random, math, time
# import pygame.gfxdraw
import pygame.math as pgmath

import clock

from missiles import Missile
from waves import Wave


pygame.init()

size = width, height = 1000, 700
black = 0, 0, 0
bg = 64, 64, 64

screen = pygame.display.set_mode(size)

things = []

a = time.time()
while 1:
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print things
			sys.exit()

		if event.type == pygame.KEYDOWN:
			pos = pygame.mouse.get_pos()

			if event.key == pygame.K_m:
				to_center = pgmath.Vector2(width/2-pos[0], height/2-pos[1])
				direction = to_center.as_polar()[1]
				things.append(Missile(pos, direction, [0, 0, width-1, height-1], random.randint(1,10), random.randint(0,2), random.randint(0,3)))

			if event.key == pygame.K_o:
				things.append(Wave(pos, random.randint(1,10), random.randint(0,2), random.randint(0,3)))
			


	screen.fill(bg)

	t = time.time()

	for thing in things:
		thing.tick_update()
		thing.draw(screen)
		if thing.dead:
			things.remove(thing)

	list1 = things[:]
	list2 = things[:]
	for thing in list1:
		if thing not in things:
			continue
		if thing.dead:
			things.remove(thing)
		for other in list2:
			if other not in things or other is thing:
				continue
			else:
				hit = False
				for i in thing.collidables:
					for j in other.collidables:
						if i.check_collision(j):
							hit = True
							break
					if hit: break
				if hit:
					if type(thing) == Missile and type(other) == Wave:
						other.absorb(thing)
						thing.dead = True
						things.remove(thing)
					elif type(thing) == Wave and type(other) == Missile:
						thing.absorb(other)
						other.dead = True
						things.remove(other)
					else:
						things.remove(thing)
						thing.dead = True
						things.remove(other)
						other.dead = True


	pygame.display.flip()

	clock.next_tick()