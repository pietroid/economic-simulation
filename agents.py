from entities import Agent
from multiset import Multiset as m
from commodities import food, fertiliser, farmerWork, factoryWork, minerals, minerWork

class Land(Agent):
    def transform(self):
        #natural daily production without fertiliser
        self.commodities += m({food})

        #daily production with fertiliser
        self.convert(
            m({fertiliser: 4, farmerWork: 1}), 
            m({food: 10})
        )

class Farmer(Agent):
    def transform(self):
        self.convert(
            {food}, 
            {farmerWork}
        )

class Market(Agent):
    pass

class Worker(Agent):
    def transform(self):
        self.convert(
            {food}, 
            {factoryWork}
        )

class Factory(Agent):
    def transform(self):
        self.convert(
            m({factoryWork: 1, minerals: 5}), 
            m({fertiliser: 5}),
            greedy = True
        )

class Miner(Agent):
    def transform(self):
        self.convert(
            {food},
            {minerWork}
        )

class Mining(Agent):
    def transform(self):
        self.convert(
            {minerWork}, 
            m({fertiliser: 5}),
            greedy = True
        )