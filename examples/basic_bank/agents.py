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
                debtInstance.interest *= 1.01
            else:
                self.intents.append(SellIntent({debtInstance}, 100 * debtInstance.interest))
                if(debtInstance.status == 'expired'):
                    #wait for response
                    pass
                else:
                    debtInstance.status = 'expired'
                    self.sendMessage(debtInstance.last_agent_id, {'status':'expired_debt','value': 100 * debtInstance.interest})

class Person(Agent):
    def __init__(self):
        super().__init__(0, m({}))

    def transform(self):
        self.intents = [
            SellIntent({debt()}, 100)
        ]
        for message in self.receivedMessages:
            if(message.content['status'] == 'expired_debt'):
                self.intents.append(BuyIntent({debt()}, message.content['value'], target_id = message.recipient_id))

        if(self.money < 50 and not self.contains({debt()})):
            self.commodities.add(debt())

        self.money += 10