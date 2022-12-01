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
        self.bread_price = 5

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
    
        self.add(BuyIntent({wood()}, 5, exchanges_limit = 2))
        self.add(BuyIntent({wheat()}, 2, exchanges_limit = 10))

        #calculate bread_price
        price_change = 0
        self.c_d = 0.1
        self.c_l1 = 3
        self.c_l2 = 0.01

        breadIntent = self.get_old_intent('bread')
        if breadIntent is not None:

            #calculate change due to demand
            qty_completed_intent = len(breadIntent.get_completed())
            qty_total_intent = len(breadIntent.get_completed()) + len(breadIntent.get_unmatched())
            if(qty_total_intent > 0):
                percentage_completed = qty_completed_intent / qty_total_intent
            else:
                percentage_completed = 1
            price_change += self.c_d * (percentage_completed - 1)
            
            #calculate change due to profit 
            if(qty_completed_intent > 0):
                print(self.old.profit)
                unit_profit = self.old.profit / qty_completed_intent
                if(unit_profit < self.c_l1):
                    price_change += self.c_l2 * (self.c_l1 - unit_profit)
                
                print(f'unit_profit: {unit_profit}')

        self.bread_price = self.old.bread_price * (1 + price_change)
       
        print(f'bread price: ${self.bread_price}')
        self.add(SellIntent({bread()}, self.bread_price, 0.1, intent_label = 'bread'))
        
        self.add(BuyIntent({artifact()},150, exchanges_limit = 1))
        super().transform()

class Farmer(Person):
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

        self.add(BuyIntent({bread()}, 10, exchanges_limit = 2))
        self.add(SellIntent({wheat()}, 2))    
        self.add(BuyIntent({artifact()},150, exchanges_limit = 1))
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
        
        self.add(BuyIntent({wood()}, 5, exchanges_limit = 10))
        self.add(BuyIntent({bread()}, 10, exchanges_limit = 1))
        self.add(SellIntent({artifact()},150))
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
        
        self.add(BuyIntent({bread()}, 10, exchanges_limit = 3))
        self.add(SellIntent({wood()}, 5))
        self.add(BuyIntent({artifact()},150, exchanges_limit = 1))
        super().transform()