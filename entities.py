import copy
from typing import List
from multiset import *

agent_debug = False
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
        self.id = f'{self.__class__.__name__}_{agent_id}'
        agent_id += 1

    def iterate(self):
        #old
        self.old = copy.deepcopy(self)
        #new
        if(agent_debug):
            print(f'last intents for {self.__class__.__name__}')
            for intent in self.intents:
                print(intent)

        #resetting
        self.intents = []
        self.messagesToSend = []
        self.transform()
        
        #resetting 
        self.receivedMessages = []

    def transform(self):
        pass

    ## convert if possible from one set of commodities to another set
    def convert(self, from_:Multiset, to:Multiset, greedy = False):
        while(self.contains(from_)):
            self.extract(from_)
            self.commodities += to
            if(not greedy): 
                break
    
    def contains(self, test_commodities: Multiset):
        commodities = copy.copy(self.commodities)
        for test_commodity in test_commodities:
            has_test_commodity = False
            for commodity in commodities:
                if(commodity.description == test_commodity.description):
                    has_test_commodity = True
                    commodities.remove(commodity, 1)
                    break
            if(not has_test_commodity):
                return False
        return True

    def extract(self, commodities_to_extract: Multiset):
        concrete_commodities_to_extract = Multiset({})
        for commodity_to_extract in commodities_to_extract:
            for commodity in self.commodities:
                if(commodity_to_extract.description == commodity.description):
                    self.commodities.remove(commodity, 1)
                    concrete_commodities_to_extract.add(commodity)
                    break
        return concrete_commodities_to_extract

    def sendMessage(self, to, message):
        self.messagesToSend.append(Message(self.id, to, message))

    def add(self, intent):
        self.intents.append(intent)

class C:
    def __init__(self, description):
        self.description = description
        self.last_agent_id = None

    def hasAttributes(self):
        return len(self.__dict__) > 2

    # def __eq__(self, other):
    #     return self.description == other.description
    
    # def __hash__(self):
    #     return hash(self.description)
        
class Intent:
    def __init__(self, commodities: Multiset, price:float = 0, exchanges_limit = float('inf'), target_id: int = None):
        self.commodities = commodities
        self.price = price
        self.exchanges_limit = exchanges_limit
        self.target_id = target_id
        self.status = {}
        self.completed_intents = 0
    
    def is_unmatched(self):
        return self.status == {}

    def add_status(self, status, target_id, data = {}):
        self.status[target_id] = {'status': status, 'data': data}


class BuyIntent(Intent):
    def __str__(self):
        return f'buy({list(get_description(self.commodities).items())}, ${self.money}, {self.status})'

class SellIntent(Intent):
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
        return f'{self.primaryAgent.id} , {self.primaryAgent.__class__.__name__.ljust(15)} <--${self.moneyFlow}--'.ljust(10,'-') + \
        f'   --{str(list(get_description(self.commoditiesFlow).items()))}'.ljust(60,'-')+f'--> {self.secondaryAgent.__class__.__name__}'

class Message:
    def __init__(self, recipient_id, destinatary_id, content):
        self.recipient_id = recipient_id
        self.destinatary_id = destinatary_id
        self.content = content

def get_description(commodities: Multiset):
    return Multiset(map(lambda commodity: commodity.description, commodities))
