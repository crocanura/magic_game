empty = set()

gray = (128,128,128)
scarlet = (255, 40, 0)
purple = (180, 0, 255)
blue = (0, 128, 255)
black = (0,0,0)
white = (255, 255, 255)

types = { }
types['a'] = types['effect'] = types[0] = { 0: None, 1:'damaging', 2: 'healing' }
types['push'] = types['b'] = types[1] = { 0: None, 1: 'impact', 2: 'chaos', 3: 'vacuum' }
types['shape'] = types['c'] = types[2] = { 0: 'missile', 1:'lightning', 2:'wave', 3:'charge', 4:'pulse'}