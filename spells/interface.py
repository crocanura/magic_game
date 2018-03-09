from spells.base_spells import types
from spells.missiles import Missile
from spells.waves import Wave
from spells.lightning import Lightning
from spells.pulses import Pulse
from spells.charges import Charge


def create_spell(caster_position, cast_point, bounds, power=1, a=0, b=0, c=0):

	shape = types[2][c]
	# a_att = types[0][a]
	# b_att = types[1][b]

	direction = (cast_point - caster_position).as_polar()[1]

	if shape == 'missile':
		return Missile(cast_point, direction, bounds, power, a, b)

	elif shape == 'wave':
		return Wave(caster_position, power, a, b)

	elif shape == 'lightning':
		return Lightning(cast_point, direction, power, a, b)

	elif shape == 'pulse':
		return Pulse(cast_point, direction, power, a, b)

	elif shape == 'charge':
		return Charge(cast_point, power, a, b)

	else: return None