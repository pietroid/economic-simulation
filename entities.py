import copy
from typing import List
from multiset import *

agent_debug = True
class Agent:
    def __init__(self, money:float = 0, commodities: Multiset = Multiset({})):
        self.money = money
        self.commodities = commodities
        self.intents = []
        self.old = copy.deepcopy(self)

    def iterate(self):
        if(agent_debug):
            print(f'Intents for {self.__class__.__name__}')
            for intent in self.intents:
                print(intent)

        self.old = copy.deepcopy(self)
        self.transform()

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

class BuyIntent:
    def __init__(self, commodities: Multiset, money:float = 0):
        self.commodities = commodities
        self.money = money
        self.status = 'unmatched'

    def __str__(self):
        return f'buy({list(Multiset(self.commodities).items())}, ${self.money}, {self.status})'

class SellIntent:
    def __init__(self, commodities: Multiset, money:float = 0):
        self.commodities = commodities
        self.money = money
        self.status = 'unmatched'

    def __str__(self):
        return f'sell({list(Multiset(self.commodities).items())}, ${self.money}, {self.status})'
class Exchange:
    def __init__(self, primaryAgent: Agent, secondaryAgent: Agent, moneyFlow:float, commoditiesFlow: Multiset, sellIntent: SellIntent, buyIntent: BuyIntent):
        self.primaryAgent = primaryAgent
        self.secondaryAgent = secondaryAgent
        self.moneyFlow = moneyFlow
        self.commoditiesFlow = commoditiesFlow
        self.buyIntent = buyIntent
        self.sellIntent = sellIntent

    def __str__(self):
        return f'{self.primaryAgent.__class__.__name__.ljust(15)} <--${self.moneyFlow}--'.ljust(10,'-') + \
        f'   --{str(list(Multiset(self.commoditiesFlow).items()))}'.ljust(60,'-')+f'--> {self.secondaryAgent.__class__.__name__}'

