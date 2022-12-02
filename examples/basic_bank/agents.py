from behaviors import buy, sell
from entities import Agent, BuyIntent, SellIntent
from multiset import Multiset as m
from examples.basic_bank.commodities import *

class Bank(Agent):
    def __init__(self):
        super().__init__(1000, m({}))
    
    def transform(self):
        for debtIntent in self.old.intents:
            if(not debtIntent.is_unmatched()):
                for id in debtIntent.status:
                    if(debtIntent.status[id] == 'completed'):
                        self.money += 100
        
        self.add(BuyIntent({debt()}, 100))
        for debtInstance in self.commodities:
            if(debtInstance.daysToExpiration > 0):
                debtInstance.daysToExpiration -= 1
                debtInstance.interest *= 1.01
            else:
                self.add(SellIntent({debtInstance}, 100 * debtInstance.interest, exchanges_limit = 1, target_id = debtInstance.last_agent_id))
                if(debtInstance.status == 'expired'):
                    #wait for response
                    pass
                else:
                    debtInstance.status = 'expired'
                    self.sendMessage(debtInstance.last_agent_id, {'status':'expired_debt','value': 100 * debtInstance.interest})

class Person(Agent):
    def __init__(self):
        super().__init__(1000, m({bread():5}))

    def transform(self):
        self.extract({debt()})
        
        for message in self.receivedMessages:
            print(message.content)
            if(message.content['status'] == 'expired_debt'):
                self.add(BuyIntent({debt()}, message.content['value'], exchanges_limit = 1, target_id = message.recipient_id))

        if(self.money < 50 and not self.contains({debt()})):
            self.commodities.add(debt())

        self.add(SellIntent({debt()}, 100))

class Baker(Person):
    def __init__(self):
        super().__init__()

    def transform(self):
        self.convert(
            m({wheat():10, wood():2, workForce():1}),
            m({bread():10}),
        )
        if(not self.contains({workForce()})):
            self.convert(
                {bread()},
                {workForce()}
            )
        
        buy(self, wood(), 5, exchanges_limit = 2)
        buy(self, wheat(), 2, exchanges_limit = 10)
        buy(self, artifact(), 50, exchanges_limit = 1)

        sell(self, bread(), 10)
        
        super().transform()

class Farmer(Person):
    def __init__(self):
        super().__init__()
        self.bread_price = 1

    def transform(self):
        self.convert(
            m({workForce():1}),
            m({wheat():20}),
        )
        if(not self.contains({workForce()})):
            self.convert(
                m({bread():3}),
                {workForce()}
            )

        buy(self, bread(), 10, exchanges_limit = 2)
        buy(self, artifact(), 20, exchanges_limit = 1)

        sell(self, wheat(), 2)

        super().transform()

class Manufacturer(Person):
    def transform(self):
        self.convert(
            m({wood():10, workForce():5}),
            m({artifact():1}),
        )
        self.convert(
            {bread()},
            {workForce()}
        )
        
        buy(self, bread(), 10, exchanges_limit = 1)
        buy(self, wood(), 5, exchanges_limit = 10)

        sell(self, artifact(), 100)
        super().transform()

class Lumberjack(Person):
    def transform(self):
        self.convert(
            m({workForce()}),
            m({wood():10}),
        )
        if(not self.contains({workForce()})):
            self.convert(
                m({bread():2}),
                {workForce()}
            )

        buy(self, bread(), 10, exchanges_limit = 3)
        buy(self, artifact(), 30, exchanges_limit = 1)

        sell(self, wood(), 5)
        super().transform()