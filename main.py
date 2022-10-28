from time import sleep
from multiset import *
from agents import *
from data import agents
from entities import BuyIntent, Exchange, SellIntent

##configs
sleepTime = 0.1
interrupt = True
debug = True

time = 1
exchanges = []
while(True):
    #Logging
    print(f'day #{time}')
    totalMoney = 0
    for agent in agents:
        print(
            f'{agent.__class__.__name__}'.ljust(15, ' ') +
            f'commodities: {list(agent.commodities.items())}'.ljust(100, ' ') +
            f'money: {agent.money}'
        )
        totalMoney += agent.money
    print(f'totalMoney: {totalMoney}')
    print()

    totalIntents = []
    #Transformations happen here
    for agent in agents:
        agent.transform()
        for intent in agent.intents:
            totalIntents.append((agent,intent))

    #Intents match happens here
    exchanges = []
    usedIntentMatches = []

    for intentPair1 in totalIntents:
        for intentPair2 in totalIntents:
            agent1 = intentPair1[0]
            agent2 = intentPair2[0] 
            intent1 = intentPair1[1]
            intent2 = intentPair2[1]

            if(agent1 != agent2 and 
               intent1.money == intent2.money and intent1.commodities == intent2.commodities):

                if(type(intent1) is SellIntent and type(intent2) is BuyIntent and (agent1, agent2) not in usedIntentMatches):
                    exchanges.append(Exchange(agent1, agent2, intent1.money, intent1.commodities))
                    usedIntentMatches.append((agent1,agent2))
                
                if(type(intent1) is BuyIntent and type(intent2) is SellIntent (agent2, agent1) not in usedIntentMatches):
                    exchanges.append(Exchange(agent2, agent1, intent1.money, intent1.commodities))
                    usedIntentMatches.append((agent2,agent1))

    #Exchanges happen here
    for exchange in exchanges:
        if(debug):
            print(str(exchange))
        if exchange.commoditiesFlow.issubset(exchange.primaryAgent.commodities) and exchange.secondaryAgent.money >= exchange.moneyFlow:
            exchange.primaryAgent.commodities -= exchange.commoditiesFlow
            exchange.secondaryAgent.commodities += exchange.commoditiesFlow
            exchange.primaryAgent.money += exchange.moneyFlow
            exchange.secondaryAgent.money -= exchange.moneyFlow

    #Next iteration
    time += 1
    sleep(0.1)
    if(interrupt):
        input()