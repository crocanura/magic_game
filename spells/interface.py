from common import *

import pygame.math as pgmath
import random as rn

from spells.missiles import Missile
from spells.waves import Wave
from spells.lightning import Lightning
from spells.pulses import Pulse
from spells.charges import Charge

import math_tools


def create_spell(caster_position, cast_point, bounds, power=1, a=0, b=0, c=0):

	shape = types['shape'][c]

	direction = (cast_point - caster_position).as_polar()[1]

	if shape == 'missile':
		return Missile(cast_point, direction, bounds, power, a, b)

	elif shape == 'wave':
		# return Wave(caster_position, power, a, b) # this is how it's supposed to be
		return Wave(cast_point, power, a, b)

	elif shape == 'lightning':
		return Lightning(cast_point, direction, power, a, b)

	elif shape == 'pulse':
		return Pulse(cast_point, direction, power, a, b)

	elif shape == 'charge':
		return Charge(cast_point, power, a, b)

	else: return None



def combined(spells, bounds):

	spells = list(spells)

	if len(spells) <= 1:
		raise Error("Can't combine 1 or less (%d) spells" % len(spells))

	nx = sum(spell.position[0] for spell in spells)
	ny = sum(spell.position[1] for spell in spells)
	position = pgmath.Vector2(nx/len(spells), ny/len(spells))

	dirs = [spell.direction for spell in spells if hasattr(spell, 'direction') and not spell.direction is None]
	if len(dirs) == 0:
		direction = rn.uniform(0,360)
	else:
		direction = sum(dirs)/len(dirs)

	# vec = position + math_tools.cartesian_from_polar(1, direction)
	
	power = sum(spell.power for spell in spells)
	a = sum(spell.a for spell in spells) % 3
	b = sum(spell.b for spell in spells) % 4
	c = sum(spell.c for spell in spells) % 5

	shape = types['shape'][c]

	if shape == 'missile':
		return Missile(position, direction, bounds, power, a, b)

	elif shape == 'wave':
		return Wave(position, power, a, b)

	elif shape == 'lightning':
		return Lightning(position, direction, power, a, b)

	elif shape == 'pulse':
		return Pulse(position, direction, power, a, b)

	elif shape == 'charge':
		return Charge(position, power, a, b)

	else: return None