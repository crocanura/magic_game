import pygame.mixer as mix
from spells.base_spells import types as spell_types

# mix.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)
mix.init(frequency=22050, size=-16, channels=2, buffer=4096)

types = ['damaging','healing', 'impact', 'vacuum', 'chaos', 'wave', 'lightning', 'charge', 'pulse', 'missile']
exceptions = ['lightning', 'pulse']

spell_shapes = ['wave', 'lightning', 'charge', 'pulse', 'missile']
spell_harms = ['damaging','healing']
spell_moves = ['impact', 'vacuum', 'chaos']

lookup = {}

base_volume = 0.40

for t in types:
	s = '%s_hit' % t
	lookup[s] = mix.Sound("./sounds/%s.wav" % s)
	lookup[s].set_volume(base_volume)


	if t in exceptions:
		s = '%s_whiff' % t
		lookup[s] = mix.Sound("./sounds/%s.wav" % s)
	else:
		s = '%s_cast' % t
		lookup[s] = mix.Sound("./sounds/%s.wav" % s)

	lookup[s].set_volume(base_volume)


lookup['missile_cast'].set_volume(base_volume/4)
# lookup['wave_cast'].set_volume(base_volume)
lookup['chaos_cast'].set_volume(base_volume/4)
lookup['vacuum_cast'].set_volume(base_volume)
lookup['impact_cast'].set_volume(base_volume*4)
lookup['charge_cast'].set_volume(base_volume*2)

lookup['missile_hit'].set_volume(base_volume/4)
# lookup['wave_hit'].set_volume(base_volume)
lookup['chaos_hit'].set_volume(base_volume/4)
lookup['vacuum_hit'].set_volume(base_volume)
lookup['impact_hit'].set_volume(base_volume*4)
lookup['charge_hit'].set_volume(base_volume*2)
lookup['healing_hit'].set_volume(base_volume*2)



def cast_sounds(spell):
	sounds = []

	if spell_types[2][spell.c] in ['lightning', 'pulse']:
		return sounds

	if spell.a > 0:
		sounds.append(lookup[spell_types[0][spell.a] + '_cast'])
	if spell.b > 0:
		sounds.append(lookup[spell_types[1][spell.b] + '_cast'])

	sounds.append(lookup[spell_types[2][spell.c] + '_cast'])

	return sounds


def hit_sounds(spell):
	sounds = []

	if spell.a > 0:
		sounds.append(lookup[spell_types[0][spell.a] + '_hit'])
	if spell.b > 0:
		sounds.append(lookup[spell_types[1][spell.b] + '_hit'])
	
	sounds.append(lookup[spell_types[2][spell.c] + '_hit'])

	return sounds


def death_sounds(spell):
	sounds = []

	if spell_types[2][spell.c] in ['lightning', 'pulse']:
		sounds.append(lookup[spell_types[2][spell.c] + '_whiff'])
	elif spell_types[2][spell.c] == 'charge':
		sounds.append(lookup['charge_hit'])

