import sys, pygame, random, math, time
# import pygame.gfxdraw
import pygame.math as pgmath
import pygame.mixer as mix

import clock

from base_spells import types as spell_types
from missiles import Missile
from waves import Wave
from lightning import Lightning

pygame.init()
from sound_loader import lookup as sound_lookup

# sound_lookup['healing_cast'].play()

size = width, height = 1000, 700
black = 0, 0, 0
bg = 64, 64, 64

screen = pygame.display.set_mode(size)

things = []

a = time.time()
quit = False
while not quit:
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print things
			quit = True
			break

		if event.type == pygame.KEYDOWN:
			pos = pygame.mouse.get_pos()
			to_center = pgmath.Vector2(width/2-pos[0], height/2-pos[1])
			direction = to_center.as_polar()[1]

			if event.key == pygame.K_m:
				things.append(Missile(pos, direction, [0, 0, width-1, height-1], random.randint(1,10), random.randint(0,2), random.randint(0,3)))
				
				a = things[-1].a
				if a > 0:
					sound_lookup[spell_types[0][a] + '_cast'].play()
				b = things[-1].b
				if b > 0:
					sound_lookup[spell_types[1][b] + '_cast'].play()
				sound_lookup['missile_cast'].play()


			if event.key == pygame.K_o:
				things.append(Wave(pos, random.randint(1,10), random.randint(0,2), random.randint(0,3)))

				a = things[-1].a
				if a > 0:
					sound_lookup[spell_types[0][a] + '_cast'].play()
				b = things[-1].b
				if b > 0:
					sound_lookup[spell_types[1][b] + '_cast'].play()
				sound_lookup['wave_cast'].play()

			if event.key == pygame.K_l:
				things.append(Lightning(pos, direction, random.randint(1,10), random.randint(0,2), random.randint(0,3)))

				# a = things[-1].a
				# if a > 0:
				# 	sound_lookup[spell_types[0][a] + '_cast'].play()
				# b = things[-1].b
				# if b > 0:
				# 	sound_lookup[spell_types[1][b] + '_cast'].play()
	
	if quit:
		pygame.quit()
		break


	screen.fill(bg)

	t = time.time()

	list1 = things
	for thing in list1:
		thing.draw(screen)
		if thing.status == 'dead':
			# print 'removing'
			things.remove(thing)
			if type(thing) == Lightning:
				sound_lookup['lightning_whiff'].play()
			continue
		thing.tick_update()

	list1 = things
	list2 = things
	for thing in list1:
		if thing not in things:
			continue
		if thing.status == 'dead':
			# things.remove(thing)
			continue
		if thing.status == 'dying':
			continue
		for other in list2:
			if (other not in things) or (other is thing) or (other.status == 'dying') or (other.status == 'dead'):
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
					if type(thing) == Missile and type(other) != Missile:
						other.absorb(thing)
						thing.status = 'dead'
						# things.remove(thing)
						continue
					elif type(thing) != Missile and type(other) == Missile:
						thing.absorb(other)
						other.status = 'dead'
						# things.remove(other)
						continue
					elif type(thing) == Missile or type(other) == Missile:
						things.remove(thing)
						thing.status = 'dead'
						things.remove(other)
						other.status = 'dead'
						continue
					# if type(thing) == Lightning:
					# 	thing.status = 'dying'
					# else:
					thing.status = 'dying'
					thing.death_animation = clock.GOAL_FPS / 4
					thing.direction = (other.position - thing.position).as_polar()[1]
					# if type(other) == Lightning:
					# 	other.status = 'dying'
					# else:
					other.status = 'dying'
					other.death_animation = clock.GOAL_FPS / 4
					other.direction = (thing.position - other.position).as_polar()[1]


	pygame.display.flip()

	clock.next_tick()