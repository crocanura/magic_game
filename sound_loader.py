import pygame.mixer as mix

# mix.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)
mix.init(frequency=22050, size=-16, channels=2, buffer=4096)

types = ['damaging','healing', 'impact', 'vacuum', 'chaos', 'wave', 'lightning', 'charge', 'pulse', 'missile']
exceptions = ['lightning', 'pulse']

spell_shapes = ['wave', 'lightning', 'charge', 'pulse', 'missile']
spell_harms = ['damaging','healing']
spell_moves = ['impact', 'vacuum', 'chaos']

lookup = {}

base_volume = 0.25

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


lookup['missile_cast'].set_volume(base_volume/10)
lookup['wave_cast'].set_volume(base_volume/4)
lookup['chaos_cast'].set_volume(base_volume/4)
lookup['vacuum_cast'].set_volume(base_volume*2.5)

lookup['missile_hit'].set_volume(base_volume/10)
lookup['wave_hit'].set_volume(base_volume/4)
lookup['chaos_hit'].set_volume(base_volume/4)