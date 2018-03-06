import random as rn

types = { }
types[0] = { 0: None, 1:'damaging', 2: 'healing' }
types[1] = { 0: None, 1: 'impact', 2: 'chaos', 3: 'vacuum' }
types[2] = { 0: 'missile', 1:'lightning', 2:'wave', 3:'charge', 4:'pulse'}

cats = list(types.keys())
for cat in cats:
    indices = list(types[cat].keys())
    for i in indices:
        typ = types[cat][i]
        types[cat][typ] = i


def random_spell(max_power=1, min_power=1):
    a = rn.randint(0,2)
    b = rn.randint(0,3)
    c = rn.randint(0,4)
    p = rn.randint(min_power, max_power)
    return Base_spell(p, a, b, c)


class Base_spell:
    def __init__(self, power=1, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
        
        self.power = power
        
        if not self.valid():
            print("Ack!")
        
    def valid(self):
        if self.a < 0 or self.b < 0 or self.c < 0:
            return False
        if self.a > 2 or self.b > 3 or self.c > 4:
            return False
        return True
        
    def combine(self, other):
        a = (self.a + other.a) % 3
        b = (self.b + other.b) % 4
        c = (self.c + other.c) % 5
        p = self.power + other.power
        return Base_spell(p, a, b, c)
    
    def __str__(self):
        st = ""
        
        st1 = types[0][self.a]
        if not st1 is None:
            st += "%s " % st1
        else:
            st += "power "
        st += "%d " % self.power
        
        
        st2 = types[1][self.b]
        if not st2 is None:
            st += "%s " % st2
        
        
        st3 = types[2][self.c]
        st += st3
        
        
        return st
    
    def __repr__(self):
        return str(self)