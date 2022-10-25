from typing import List
from multiset import *

class Commodity:
    def __init__(self, name:str, description: str):
        self.name = name
        self.description = description

class Agent:
    def __init__(self, money:float, commodities: Multiset):
        self.money = money
        self.commodities = commodities

    def transform(self):
        return self


class Exchange:
    def __init__(self, primaryAgent: Agent, secondaryAgent: Agent, moneyFlow:float, commoditiesFlow: Multiset):
        self.primaryAgent = primaryAgent
        self.secondaryAgent = secondaryAgent
        self.moneyFlow = moneyFlow
        self.commoditiesFlow = commoditiesFlow