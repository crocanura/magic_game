import sys, pygame, random, math, time
# import pygame.gfxdraw
import pygame.math as pgmath
import pygame.mixer as mix

import clock

from spells.base_spells import types as spell_types
import spells.interface

pygame.init()
from sound_loader import lookup as sound_lookup
import sound_loader

# sound_lookup['healing_cast'].play()

size = width, height = 1000, 700
black = 0, 0, 0
bg = 64, 64, 64

screen = pygame.display.set_mode(size)

key_to_c = {}
key_to_c[pygame.K_m] = spell_types[2]['missile']
key_to_c[pygame.K_o] = spell_types[2]['wave']
key_to_c[pygame.K_l] = spell_types[2]['lightning']
key_to_c[pygame.K_p] = spell_types[2]['pulse']
key_to_c[pygame.K_k] = spell_types[2]['charge']

quit = False

recipe = [0, 0, 0, 0]

living_spells = []

while not quit:
	

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			print living_spells
			quit = True
			break

		if event.type == pygame.KEYDOWN:

			if event.key == pygame.K_1:
				recipe[0] = (recipe[0] + 1) % 3
				print "Spell attribute a set to %s" % spell_types[0][recipe[0]]
			if event.key == pygame.K_2:
				recipe[1] = (recipe[1] + 1) % 4
				print "Spell attribute a set to %s" % spell_types[1][recipe[1]]
			if event.key == pygame.K_3:
				recipe[2] = (recipe[2] + 1) % 5
				print "Spell attribute a set to %s" % spell_types[2][recipe[2]]
			# if event.key == pygame.K_4:
				

		
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 3:
				recipe[3] += 1
				print "Spell power set to %s" % recipe[3]
				continue
			elif event.button == 4:
				recipe[3] += 1
				print "Spell power set to %s" % recipe[3]
				continue
			elif event.button == 5:
				recipe[3] = max(0, recipe[3] - 1)
				print "Spell power set to %s" % recipe[3]
				continue
			elif event.button != 1:
				continue
				
			if recipe[3] <= 0:
				continue

			cast_point = pgmath.Vector2(pygame.mouse.get_pos())
			# to_center = pgmath.Vector2(width/2-pos[0], height/2-pos[1])
			# direction = to_center.as_polar()[1]

			player_pos = pgmath.Vector2(width/2, height/2) # wild accusations
			bounds = [0,0, width - 1, height - 1]

			# a = spell_types[0][recipe[0]]
			# b = spell_types[1][recipe[1]]
			# c = spell_types[2][recipe[2]]
			spell = spells.interface.create_spell(player_pos, cast_point, bounds, recipe[3], recipe[0], recipe[1], recipe[2])
			recipe[3] = 0

			sounds = sound_loader.cast_sounds(spell)
			for s in sounds: s.play()

			living_spells.append(spell)



			# if event.key == pygame.K_m:
			# 	things.append(Missile(pos, direction, [0, 0, width-1, height-1], random.randint(1,10), random.randint(0,2), random.randint(0,3)))
				
			# 	a = things[-1].a
			# 	if a > 0:
			# 		sound_lookup[spell_types[0][a] + '_cast'].play()
			# 	b = things[-1].b
			# 	if b > 0:
			# 		sound_lookup[spell_types[1][b] + '_cast'].play()
			# 	sound_lookup['missile_cast'].play()


			# if event.key == pygame.K_o:
			# 	things.append(Wave(pos, random.randint(1,10), random.randint(0,2), random.randint(0,3)))

			# 	a = things[-1].a
			# 	if a > 0:
			# 		sound_lookup[spell_types[0][a] + '_cast'].play()
			# 	b = things[-1].b
			# 	if b > 0:
			# 		sound_lookup[spell_types[1][b] + '_cast'].play()
			# 	sound_lookup['wave_cast'].play()

			# if event.key == pygame.K_k:
			# 	things.append(Charge(pos, random.randint(1,10), random.randint(0,2), random.randint(0,3)))

			# 	a = things[-1].a
			# 	if a > 0:
			# 		sound_lookup[spell_types[0][a] + '_cast'].play()
			# 	b = things[-1].b
			# 	if b > 0:
			# 		sound_lookup[spell_types[1][b] + '_cast'].play()
			# 	sound_lookup['charge_cast'].play()

			# if event.key == pygame.K_l:
			# 	things.append(Lightning(pos, direction, random.randint(1,10), random.randint(0,2), random.randint(0,3)))

			# if event.key == pygame.K_p:
			# 	things.append(Pulse(pos, direction, random.randint(1,10), random.randint(0,2), random.randint(0,3)))

	
	if quit:
		pygame.quit()
		break


	screen.fill(bg)

	ls = living_spells
	for spell in ls:
		if spell.status == 'dead':
			living_spells.remove(spell)
			sounds = sound_loader.hit_sounds(spell)
			for s in sounds:
				s.play()
		else:
			spell.draw(screen)
			spell.tick_update()

	t = time.time()



	# list1 = things
	# for thing in list1:
	# 	thing.draw(screen)
	# 	if thing.status == 'dead':
	# 		# print 'removing'
	# 		things.remove(thing)
	# 		if type(thing) == Lightning:
	# 			sound_lookup['lightning_whiff'].play()
	# 		if type(thing) == Pulse:
	# 			sound_lookup['pulse_whiff'].play()
	# 		continue
	# 	thing.tick_update()

	# list1 = things
	# list2 = things
	# for thing in list1:
	# 	if thing not in things:
	# 		continue
	# 	if thing.status == 'dead':
	# 		# things.remove(thing)
	# 		continue
	# 	if thing.status == 'dying':
	# 		continue
	# 	for other in list2:
	# 		if (other not in things) or (other is thing) or (other.status == 'dying') or (other.status == 'dead'):
	# 			continue
	# 		else:
	# 			hit = False
	# 			for i in thing.collidables:
	# 				for j in other.collidables:
	# 					if i.check_collision(j):
	# 						hit = True
	# 						break
	# 				if hit: break
	# 			if hit:
	# 				print "HIT!"
	# 				if type(thing) == Missile and type(other) != Missile:
	# 					other.absorb(thing)
	# 					thing.status = 'dead'
	# 					# things.remove(thing)
	# 					continue
	# 				elif type(thing) != Missile and type(other) == Missile:
	# 					thing.absorb(other)
	# 					other.status = 'dead'
	# 					# things.remove(other)
	# 					continue
	# 				elif type(thing) == Missile or type(other) == Missile:
	# 					things.remove(thing)
	# 					thing.status = 'dead'
	# 					things.remove(other)
	# 					other.status = 'dead'
	# 					continue
	# 				# if type(thing) == Lightning:
	# 				# 	thing.status = 'dying'
	# 				# else:
					
	# 				thing.status = 'dead'
	# 				# thing.death_animation = clock.GOAL_FPS / 4
	# 				# thing.direction = (other.position - thing.position).as_polar()[1]
	# 				# if type(other) == Lightning:
	# 				# 	other.status = 'dying'
	# 				# else:

	# 				other.status = 'dead'
	# 				# other.death_animation = clock.GOAL_FPS / 4
	# 				# other.direction = (thing.position - other.position).as_polar()[1]


	pygame.display.flip()

	clock.next_tick()