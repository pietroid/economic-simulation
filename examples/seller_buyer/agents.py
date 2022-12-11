from behaviors import buy, sell
from entities import Agent, BuyIntent, SellIntent
from multiset import Multiset as m
from examples.seller_buyer.commodities import *

class Producer1(Agent):
    def __init__(self):
        super().__init__(1000)
    
    def transform(self):
        self.convert({},m({product1(): 10}))
        sell(self, product1(), 5)

class Producer2(Agent):
    def __init__(self):
        super().__init__(1000)
    
    def transform(self):
        buy(self, product1(), 10)