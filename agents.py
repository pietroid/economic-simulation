from entities import Agent
from multiset import Multiset as m
from commodities import food, fertiliser, farmerWork, factoryWork, minerals, minerWork

class Land(Agent):
    def transform(self):
        #natural daily production without fertiliser
        self.commodities += m({food})

        #daily production with fertiliser
        self.convert(
            m({fertiliser: 1, farmerWork: 1}), 
            m({food: 10})
        )
class Factory(Agent):
    def transform(self):
        self.convert(
            m({factoryWork: 1, minerals: 5}), 
            m({fertiliser: 5}),
            greedy = True
        )
class Mining(Agent):
    def transform(self):
        self.convert(
            {minerWork}, 
            m({minerals: 5}),
            greedy = True
        )

class Market(Agent):
    pass
class BaseWorker(Agent):
    def __init__(self, workForce, money:float = 0, commodities: m = m({})):
        super().__init__(money,commodities)
        self.workForce = workForce
    
    def transform(self):
        if(self.contains({self.workForce})):
            to = m({})
        else:
            to = m({self.workForce})
        self.convert(
            {food}, 
            to
        )
class Farmer(BaseWorker):
    def __init__(self, money:float = 0, commodities: m = m({})):
        super().__init__(farmerWork, money,commodities)

class Worker(BaseWorker):
    def __init__(self, money:float = 0, commodities: m = m({})):
        super().__init__(factoryWork, money, commodities)

class Miner(BaseWorker):
    def __init__(self, money:float = 0, commodities: m = m({})):
        super().__init__(minerWork, money, commodities)



