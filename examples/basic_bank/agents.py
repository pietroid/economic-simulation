from entities import Agent, BuyIntent, SellIntent
from multiset import Multiset as m
from examples.basic_bank.commodities import debt

class Bank(Agent):
    def __init__(self):
        super().__init__(100, m({}))
    
    def transform(self):
        self.intents = [
            BuyIntent({debt()}, 100)
        ]

        for debtInstance in self.commodities:
            if(debtInstance.daysToExpiration > 0):
                debtInstance.daysToExpiration -= 1
            else:
                debtInstance.status = 'expired'
                self.intents.append(SellIntent({debtInstance}, 100 * debtInstance.interest))
            debtInstance.interest *= 1.01

class Person(Agent):
    def __init__(self):
        super().__init__(0, m({}))

    def transform(self):
        if(self.money == 0 and not self.contains({debt()})):
            self.commodities.add(debt())
        
        self.intents = [
            SellIntent({debt()}, 100)
        ]