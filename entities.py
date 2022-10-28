from ast import Mult
import re
from typing import List
from multiset import *

class Agent:
    def __init__(self, money:float = 0, commodities: Multiset = Multiset({})):
        self.money = money
        self.commodities = commodities
        self.intents = []

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

    def __str__(self):
        return f'{self.primaryAgent.__class__.__name__.ljust(15)} <--${self.moneyFlow}--'.ljust(10,'-') + \
        f'   --{str(list(Multiset(self.commoditiesFlow).items()))}'.ljust(60,'-')+f'--> {self.secondaryAgent.__class__.__name__}'

class BuyIntent:
    def __init__(self, commodities: Multiset, money:float = 0):
        self.commodities = commodities
        self.money = money

    def __str__(self):
        return f'buy({list(self.commodities.items())},{self.money})'

class SellIntent:
    def __init__(self, commodities: Multiset, money:float = 0):
        self.commodities = commodities
        self.money = money

    def __str__(self):
        return f'sell({list(self.commodities.items())},{self.money})'