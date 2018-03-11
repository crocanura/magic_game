from common import *

import random as rn
import pygame.math as pgmath
from game_objects import Game_object

a_colours = [None, black, white]
b_colours = [None, scarlet, purple, blue]


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
    return Base_spell(0, 0, 0, p, a, b, c)



class Base_spell(Game_object):
    def __init__(self, power=1, a=0, b=0, c=0, position=(0,0)):
        Game_object.__init__(self, position)

        self.a = a
        self.b = b
        self.c = c
        
        self.power = power

        # self.lives_inside = [] # waves to provide opposite envelopment hits
        
        if not self.valid():
            print("Ack!")

        
    def valid(self):
        if self.a < 0 or self.b < 0 or self.c < 0:
            return False
        if self.a > 2 or self.b > 3 or self.c > 4:
            return False
        return True
    

    def absorb(self, other): # should probably only be used on missiles
        self.a = (self.a + other.a) % 3
        self.b = (self.b + other.b) % 4
        self.c = (self.c + other.c) % 5
        self.power = self.power + other.power


    def colouring(self):
        """Returns two tuples: inner colour and outline colour"""
        ca = a_colours[self.a]
        cb = b_colours[self.b]

        if ca is None:
            if not cb is None:
                return (cb, cb)
            else:
                return (gray, gray)

        if cb is None and not ca is None:
            return (ca, ca)

        return (ca, cb)

    
    def spell_attribute(self, x):
        if x in [0, 'a', 'effect']:
            return types[0][self.a]
        if x in [1, 'b', 'push']:
            return types[1][self.b]
        if x in [2, 'c', 'shape']:
            return types[2][self.c]

    
    def __str__(self):
        st = ""

        if self.status != 'living':
            st += self.status + " "
        
        st1 = types[0][self.a]
        if not st1 is None:
            st += "%s " % st1
        else:
            st += "power "
        # print self.power
        st += "%d " % self.power
        
        
        st2 = types[1][self.b]
        if not st2 is None:
            st += "%s " % st2
        
        
        st3 = types[2][self.c]
        st += st3
        
        
        return st
    
    def __repr__(self):
        return str(self)



def combine(spell1, spell2):
        a = (spell1.a + spell2.a) % 3
        b = (spell1.b + spell2.b) % 4
        c = (spell1.c + spell2.c) % 5
        p = spell1.power + spell2.power

        return Base_spell(p, a, b, c, (0,0))