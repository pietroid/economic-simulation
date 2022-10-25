from typing import List
class Commodity:
    def __init__(self, name:str, description: str, quantity: float = 1.0):
        self.name = name
        self.description = description
        self.quantity = quantity

class Agent:
    def __init__(self, money:float, commodities: List[Commodity]):
        self.money = money
        self.commodities = commodities

class Transformation:
    def __init__(self, initialAgent: Agent, finalAgent: Agent):
        self.initialAgent = initialAgent
        self.finalAgent = finalAgent

class Exchange:
    def __init__(self, primaryAgent: Agent, secondaryAgent: Agent, moneyFlow:float, commoditiesFlow: List[Commodity]):
        self.primaryAgent = primaryAgent
        self.secondaryAgent = secondaryAgent
        self.moneyFlow = moneyFlow
        self.commoditiesFlow = commoditiesFlow