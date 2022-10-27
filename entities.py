from typing import List
from multiset import *

class Agent:
    def __init__(self, money:float = 0, commodities: Multiset = Multiset({})):
        self.money = money
        self.commodities = commodities

    def transform(self):
        pass

    ## convert if possible from one set of commodities to another set
    def convert(self, from_:Multiset, to:Multiset, greedy = False):
        while(from_.issubset(self.commodities)):
            self.commodities -= from_
            self.commodities += to
            if(not greedy): 
                break
    
    def contains(self, commodities: Multiset):
        return commodities.issubset(self.commodities)

class Exchange:
    def __init__(self, primaryAgent: Agent, secondaryAgent: Agent, moneyFlow:float, commoditiesFlow: Multiset):
        self.primaryAgent = primaryAgent
        self.secondaryAgent = secondaryAgent
        self.moneyFlow = moneyFlow
        self.commoditiesFlow = commoditiesFlow