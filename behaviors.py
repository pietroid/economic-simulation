from entities import C, Agent, BuyIntent, SellIntent
import random

######################################################################
##                                                                  ##
##    BEHAVIORS: set of common functions that can be used by any    ##
##    agent. These functions reflect complex internal agent         ##
##    decisions, with generally lots of agent variables involved    ##
##                                                                  ##
######################################################################




######################################################################
##                                                                  ##
##    SELL A COMMODITY WITH DEFAULT PRICE DYNAMICS                  ##
##    1. PRICE DYNAMIC CHANGE DUE TO DEMAND                         ##
##    2. PRICE DYNAMIC CHANGE DUE TO PROFIT                         ##
##                                                                  ##
######################################################################

def sell(self: Agent, commodity:C, initial_price: float, exchanges_limit = float('inf')):
    
    #CONSTANTS
    price_change = 0
    commodity_label = commodity.description
    
    if(hasattr(self, 'old') and hasattr(self.old, 'old') and hasattr(self.old.old, 'profit')):
        if(self.old.profit <= self.old.old.profit):
            self.c_d = self.old.c_d * (1 + random.uniform(-0.1, 0.1))
            self.c_l1 = self.old.c_l1 * (1 + random.uniform(-0.1, 0.1))
            self.c_l2 = self.old.c_l2 * (1 + random.uniform(-0.1, 0.1))
    else:
        self.c_d = 0.1
        self.c_l1 = 5
        self.c_l2 = 0.01
    
    print(f'sell c_d: {self.c_d} c_l1: {self.c_l1} c_l2: {self.c_l2}')

    oldIntent = self.get_old_intent(commodity_label)
    if oldIntent is not None:

        # CALCULATE PRICE CHANGE DUE TO DEMAND
        # it tends to lower the sell price if few people want to buy
        # the commodity for that price

        qty_completed_intent = len(oldIntent.get_completed())
        qty_total_intent = len(oldIntent.get_completed()) + len(oldIntent.get_unmatched())
        if(qty_total_intent > 0):
            percentage_completed = qty_completed_intent / qty_total_intent
        else:
            percentage_completed = 1
        price_change += self.c_d * (percentage_completed - 1)
        
        # CALCULATE PRICE CHANGE DUE TO PROFIT
        # it tends to raise the sell price if agent is losing profit
        if(qty_completed_intent > 0):
            #TODO: correct qty_completed_intent because it only reflects n of intents not n of products sold
            unit_profit = self.old.profit / qty_completed_intent
            if(unit_profit < self.c_l1):
                price_change += self.c_l2 * (self.c_l1 - unit_profit)

    if(price_change <= -0.9):
        price_change = -0.9
    
    if(hasattr(self.old, 'commodity_price')):
        old_commodity_price = self.old.commodity_price
    else:
        old_commodity_price = initial_price

    self.commodity_price = old_commodity_price * (1 + price_change)
    print(f'sell price of {commodity_label} for {self.id}: ${self.commodity_price}')
    self.add(SellIntent({commodity}, self.commodity_price, 0.1, intent_label = commodity_label, exchanges_limit = exchanges_limit))







######################################################################
##                                                                  ##
##    BUY A COMMODITY WITH DEFAULT PRICE DYNAMICS                   ##
##    1. PRICE DYNAMIC CHANGE DUE TO NECESSITY                      ##
##    2. PRICE DYNAMIC CHANGE DUE TO PROFIT                         ##
##                                                                  ##
######################################################################

def buy(self: Agent, commodity:C, initial_price: float, exchanges_limit = float('inf')):
    
    #CONSTANTS
    price_change = 0
    commodity_label = commodity.description

    if(hasattr(self, 'old') and hasattr(self.old, 'old') and hasattr(self.old.old, 'profit')):
        if(self.old.profit <= self.old.old.profit):
            self.c_n = self.old.c_n * (1 + random.uniform(-0.1, 0.1))
            self.c_l1 = self.old.c_l1 * (1 + random.uniform(-0.1, 0.1))
            self.c_l2 = self.old.c_l2 * (1 + random.uniform(-0.1, 0.1))
    else:
        self.c_n = 0.01
        self.c_l1 = 3
        self.c_l2 = 0.01

    print(f'buy c_n: {self.c_n} c_l1: {self.c_l1} c_l2: {self.c_l2}')

    # CALCULATE PRICE CHANGE DUE TO NECESSITY
    # it tends to raise the buy price if agent has
    # been without the commodity for some time

    sum = 0
    t = 0
    d = 5
        
    agent = self
    while(hasattr(agent, 'old') and t < d):
        oldIntent = agent.get_old_intent(commodity_label)
        if(oldIntent is not None):
            qty_uncompleted_intent = len(oldIntent.get_unmatched())
            qty_total_intent = len(oldIntent.get_completed()) + len(oldIntent.get_unmatched())
            if(qty_total_intent > 0):
                sum += qty_uncompleted_intent / qty_total_intent
            else:
                sum += 1
        agent = agent.old
        t += 1

    price_change += self.c_n * sum


    # CALCULATE PRICE CHANGE DUE TO PROFIT
    # it tends to lower the buy price if agent is losing profit

    oldIntent = self.get_old_intent(commodity_label)
    if oldIntent is not None:        
        qty_completed_intent = len(oldIntent.get_completed())
        if(qty_completed_intent > 0):
            #TODO: correct qty_completed_intent because it only reflects n of intents not n of products sold
            unit_profit = self.old.profit / qty_completed_intent
            if(unit_profit < self.c_l1):
                price_change += self.c_l2 * (unit_profit - self.c_l1)

    if(price_change <= -0.9):
        price_change = -0.9

    if(hasattr(self.old, 'commodity_price')):
        old_commodity_price = self.old.commodity_price
    else:
        old_commodity_price = initial_price

    self.commodity_price = old_commodity_price * (1 + price_change)
    print(f'buy price of {commodity_label} for {self.id}: ${self.commodity_price}')
    self.add(BuyIntent({commodity}, self.commodity_price, 0.1, intent_label = commodity_label, exchanges_limit = exchanges_limit))
