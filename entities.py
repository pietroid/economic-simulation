import copy
from typing import List
from multiset import *

agent_debug = True
agent_id = 0
class Agent:
    def __init__(self, money:float = 0, commodities: Multiset = Multiset({})):
        global agent_id
        self.money = money
        self.commodities = commodities
        self.intents = []
        self.messagesToSend = []
        self.receivedMessages = []
        self.old = copy.deepcopy(self)
        self.id = agent_id
        agent_id += 1

    def iterate(self):
        if(agent_debug):
            print(f'Intents for {self.__class__.__name__}')
            for intent in self.intents:
                print(intent)

        self.old = copy.deepcopy(self)
        self.transform()

    def transform(self):
        pass

    ## convert if possible from one set of commodities to another set
    def convert(self, from_:Multiset, to:Multiset, greedy = False):
        while(from_.issubset(self.commodities)):
            self.commodities -= from_
            self.commodities += to
            if(not greedy): 
                break
    
    def contains(self, test_commodities: Multiset):
        return test_commodities.issubset(self.commodities)

    def sendMessage(self, to, message):
        self.messagesToSend.append(Message(self.id, to, message))

class C:
    def __init__(self, description):
        self.description = description
        self.last_agent_id = None

    def hasAttributes(self):
        return len(self.__dict__) > 2

    def __eq__(self, other):
        return self.description == other.description
    
    def __hash__(self):
        return hash(self.description)
        
class BuyIntent:
    def __init__(self, commodities: Multiset, money:float = 0, target_id: int = None):
        self.commodities = commodities
        self.money = money
        self.target_id = target_id
        self.status = 'unmatched'

    def __str__(self):
        return f'buy({list(get_description(self.commodities).items())}, ${self.money}, {self.status})'

class SellIntent:
    def __init__(self, commodities: Multiset, money:float = 0, target_id: int = None):
        self.commodities = commodities
        self.money = money
        self.target_id = target_id
        self.status = 'unmatched'

    def __str__(self):
        return f'sell({list(get_description(self.commodities).items())}, ${self.money}, {self.status})'
class Exchange:
    def __init__(self, primaryAgent: Agent, secondaryAgent: Agent, moneyFlow:float, commoditiesFlow: Multiset, sellIntent: SellIntent, buyIntent: BuyIntent):
        self.primaryAgent = primaryAgent
        self.secondaryAgent = secondaryAgent
        self.moneyFlow = moneyFlow
        self.commoditiesFlow = commoditiesFlow
        self.buyIntent = buyIntent
        self.sellIntent = sellIntent

    def __str__(self):
        return f'{self.primaryAgent.__class__.__name__.ljust(15)} <--${self.moneyFlow}--'.ljust(10,'-') + \
        f'   --{str(list(get_description(self.commoditiesFlow).items()))}'.ljust(60,'-')+f'--> {self.secondaryAgent.__class__.__name__}'

class Message:
    def __init__(self, recipient_id, destinatary_id, content):
        self.recipient_id = recipient_id
        self.destinatary_id = destinatary_id
        self.content = content

def get_description(commodities: Multiset):
    return Multiset(map(lambda commodity: commodity.description, commodities))
