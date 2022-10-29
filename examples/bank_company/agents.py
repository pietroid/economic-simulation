from lib2to3.pytree import convert
from entities import Agent, BuyIntent, SellIntent
from multiset import Multiset as m
from examples.bank_company.commodities import debt, workForce, rawMaterial, product

class Bank(Agent):
    def __init__(self):
        super().__init__(100, m({}))
        self.debtIntent = BuyIntent({debt}, 100)
    
    def transform(self):
        self.debtCompleted = self.old.debtIntent.status == 'completed'
        
        if(self.debtCompleted):
            self.money += 100

        self.debtIntent = BuyIntent({debt}, 100)
        self.intents = [
            self.debtIntent
        ]

class Company(Agent):
    def __init__(self):
        super().__init__(0, m({}))
        self.salary = 1
        self.materialPrice = 1
        self.workForceIntent = BuyIntent({workForce}, self.salary)
        self.rawMaterialIntent = BuyIntent({rawMaterial}, self.materialPrice)
    
    def transform(self):
        self.intents = []

        #wants to lend money
        if(self.money == 0 and not self.contains(m({debt: 1}))):
            self.commodities += {debt}
            self.intents.append(SellIntent({debt}, 100))

        #if money, pay people and but material
        if(self.money > 0):
            #increase salary if not people
            if(self.old.workForceIntent.status == 'unmatched'):
                self.salary += 1
            self.workForceIntent = BuyIntent({workForce}, self.salary)
            self.intents.append(self.workForceIntent)
        
            #increase salary if not material
            if(self.old.rawMaterialIntent.status == 'unmatched'):
                self.materialPrice += 1
            self.rawMaterialIntent = BuyIntent({rawMaterial}, self.materialPrice)
            self.intents.append(self.rawMaterialIntent)

        #if worker and material, do stuff
        self.convert(m({workForce, rawMaterial}), m({product}))


class Worker(Agent):
    def __init__(self):
        super().__init__(0, m({}))
        self.salary = 6
        self.workForceIntent = SellIntent({workForce}, self.salary)

    def transform(self):

        if(not self.contains({workForce})):
            self.commodities += m({workForce})
        
        if(self.old.workForceIntent.status == 'unmatched'):
            self.salary -= 1
        
        self.workForceIntent = SellIntent({workForce}, self.salary)
        self.intents = [
            self.workForceIntent
        ]

class MaterialProvider(Agent):
    def __init__(self):
        super().__init__(0, m({}))

    def transform(self):
        self.commodities += {rawMaterial}
        self.intents = [
            SellIntent({rawMaterial}, 3)
        ]
