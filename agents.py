from entities import Agent, BuyIntent, SellIntent
from multiset import Multiset as m
from commodities import food, fertiliser, farmerWork, factoryWork, minerals, minerWork

class Land(Agent):
    def transform(self):
        #natural daily production without fertiliser
        self.commodities += m({food:1})

        #daily production with fertiliser
        self.convert(
            m({fertiliser: 1, farmerWork: 1}), 
            m({food: 10}),
            greedy = True,
        )

        self.intents = [
            BuyIntent({farmerWork}),
            BuyIntent({fertiliser}),
            SellIntent({food})
        ]

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
    def __init__(self, money:float = 0, commodities: m = m({})):
        self.constantCommoditiesTime = 0 
        self.buyIntent = BuyIntent({food}, 10)
        super().__init__(money,commodities)
        
    def transform(self):
        if(self.old.buyIntent.status == 'unmatched'):
            self.constantCommoditiesTime += 1 
        else:
            self.constantCommoditiesTime = 0
    
        if(self.constantCommoditiesTime == 5):
            self.buyIntent.money += 1
            self.constantCommoditiesTime = 0

        self.intents = [
            self.buyIntent
        ]

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

    def transform(self):
        self.intents = [
            SellIntent({farmerWork}),
            SellIntent({fertiliser}),
            BuyIntent({food}),
            SellIntent({food}, 15)
        ]

        return super().transform()

class Worker(BaseWorker):
    def __init__(self, money:float = 0, commodities: m = m({})):
        super().__init__(factoryWork, money, commodities)

class Miner(BaseWorker):
    def __init__(self, money:float = 0, commodities: m = m({})):
        super().__init__(minerWork, money, commodities)



