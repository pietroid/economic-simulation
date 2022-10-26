from entities import Agent
from multiset import *

class Land(Agent):
    def __init__(self):
        Agent.__init__(self, 0, Multiset({}))
    
    def transform(self):
        self.commodities += Multiset({'food'})

class Farmer(Agent):
    def __init__(self):
        Agent.__init__(self, 0, Multiset({}))

class Bank(Agent):
    def __init__(self):
        Agent.__init__(self, 1000, Multiset({}))