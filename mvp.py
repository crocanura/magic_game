from common import *

import clock
import spells.interface
import collider
import math_tools

import sys, pygame, random, math, time

import pygame.math as pgmath
import pygame.mixer as mix

pygame.init()
mix.init(frequency=22050, size=-16, channels=16, buffer=4096)
from sound_loader import lookup as sound_lookup
import sound_loader

# sound_lookup['healing_cast'].play()
black = 0, 0, 0
bg = 64, 64, 64

key_to_c = {}
key_to_c[pygame.K_m] = types['shape']['missile']
key_to_c[pygame.K_o] = types['shape']['wave']
key_to_c[pygame.K_l] = types['shape']['lightning']
key_to_c[pygame.K_p] = types['shape']['pulse']
key_to_c[pygame.K_k] = types['shape']['charge']


class Game(object):
	def __init__(self, width=1000, height=800):

		self.width, self.height = width, height
		self.bounds = [0,0, width - 1, height - 1]

		size = width, height
		self.screen = pygame.display.set_mode(size)

		self.spell_set = set()
		self.objects = set()


	def get_spells(self, func = lambda spell: True):
		return list(filter(func, self.spell_set))


	def get_objects(self, func = lambda obj: True):
		return list(filter(func, self.objects))


	def living_waves(self):
		return list(filter(lambda spell: types['shape'][spell.c] == 'wave' and spell.status == 'living', self.spell_set))


	def add_object(self, obj):
		self.objects.add(obj)


	def add_spell(self, spell):
		self.add_object(spell)

		for wave in self.living_waves():
			for c in spell.collidables:
				if c.type == 'circle':
					# print "looking at %s is a %s" % (c, 'circle')
					if math_tools.circle_enveloped_by_circle(c.center, c.radius, wave.position, wave.radius):
						wave.should_contain.add(spell)
						# print "%s should contain %s" % (wave, spell)
						break
				elif c.type == 'segment':
					# print "looking at %s is a %s" % (c, 'segment')
					if math_tools.segment_enveloped_by_circle(c.p1, c.p2, wave.position, wave.radius):
						wave.should_contain.add(spell)
						# print "%s should contain %s" % (wave, spell)
						break
				elif c.type == 'point':
					# print "looking at %s is a %s" % (c, 'point')
					if c.point.distance_to(wave.position) < wave.radius:
						wave.should_contain.add(spell)
						# print "%s should contain %s" % (wave, spell)
						break

		self.spell_set.add(spell)


	def update(self, func = lambda obj: True):
		for obj in list(filter(func, self.objects)):
			obj.tick_update()


	def draw(self, func = lambda obj: True):
		for obj in list(filter(func, self.objects)):
			obj.draw(self.screen)


	def purge(self, func = lambda obj: True):
		for obj in list(filter(func, self.objects)):
			self.objects.remove(obj)
			if obj in self.spell_set:
				self.spell_set.remove(obj)


	def spell_collision_step(self):
		spell_list = self.get_spells(lambda spell: spell.status == 'living')
		collider.reset_collisions(spell_list)
		blobs = collider.collision_blobs(spell_list)
		if blobs != []:
			print ""
		for line in blobs:
			print "found collision blob: %s" % str(line)
		if blobs != []:
			print ""

		for blob in blobs:
			if len(blob) <= 1:
				print "length %d blob" % len(blob)
				sys.exit()
			elif len(blob) == 2:
				if blob[0].spell_attribute('shape') == 'missile' and blob[1].spell_attribute('shape') != 'missile':
					blob[1].absorb(blob[0])
					blob[0].kill()
					blob[0].silence()
					continue
				if blob[1].spell_attribute('shape') == 'missile' and blob[0].spell_attribute('shape') != 'missile':
					blob[0].absorb(blob[1])
					blob[1].kill()
					blob[0].silence()
					continue

			new_spell = spells.interface.combined(blob, self.bounds)
			print "Created new spell: %s" % new_spell
			self.add_spell(new_spell)
			sounds = sound_loader.cast_sounds(new_spell)
			for s in sounds: s.play()
			for spell in blob:
				spell.kill()
				# if spell.spell_attribute('shape') not in ['lightning', 'pulse']:
				# 	spell.silence()
				# self.spell_set.remove(spell)


	def run(self):

		quit = False

		recipe = [0, 0, 0, 1]

		while not quit:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					print self.spell_set
					quit = True
					break

				if event.type == pygame.KEYDOWN:

					if event.key == pygame.K_1:
						recipe[0] = (recipe[0] + 1) % 3
						print "Spell attribute a set to %s" % types[0][recipe[0]]
					if event.key == pygame.K_2:
						recipe[1] = (recipe[1] + 1) % 4
						print "Spell attribute a set to %s" % types[1][recipe[1]]
					if event.key == pygame.K_3:
						recipe[2] = (recipe[2] + 1) % 5
						print "Spell attribute a set to %s" % types[2][recipe[2]]
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

					player_pos = pgmath.Vector2(self.width/2, self.height/2) # wild accusations

					spell = spells.interface.create_spell(player_pos, cast_point, self.bounds, recipe[3], recipe[0], recipe[1], recipe[2])
					recipe[3] = 1

					sounds = sound_loader.cast_sounds(spell)
					for s in sounds: s.play()

					self.add_spell(spell)

			
			if quit:
				pygame.quit()
				break


			self.screen.fill(bg)

			self.update(lambda obj: True)

			for spell in self.get_spells(lambda spell: spell.status == 'dead'):
				if not spell.silenced:
					sounds = sound_loader.death_sounds(spell)
					for s in sounds:
						s.play()
				self.spell_set.remove(spell)
				self.objects.remove(spell)

			self.spell_collision_step()
			
			self.draw(lambda obj: True)

			# ls = self.get_spells()
			# for spell in ls:
			# 	spell.tick_update()
			# 	spell.draw(screen)

			# 	if spell.status == 'dead':
			# 		living_spells.remove(spell)
			# 		sounds = sound_loader.hit_sounds(spell)
			# 		for s in sounds:
			# 			s.play()

			t = time.time()



			
			pygame.display.flip()

			clock.next_tick()


G = Game()
G.run()