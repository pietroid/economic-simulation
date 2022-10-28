from time import sleep
from multiset import *
from agents import *
from data import agents
from entities import BuyIntent, Exchange, SellIntent

##configs
sleepTime = 0.01
interrupt = True
debug = False

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
        agent.iterate()
        for intent in agent.intents:
            if(debug):
                print(intent)
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

                if(type(intent1) is SellIntent and type(intent2) is BuyIntent and (agent1,intent1,agent2,intent2) not in usedIntentMatches):
                    exchanges.append(Exchange(agent1, agent2, intent1.money, intent1.commodities, intent1, intent2))
                    intent1.status = 'matched'
                    intent2.status = 'matched'
                    usedIntentMatches.append((agent1,intent1,agent2,intent2))
                
                if(type(intent1) is BuyIntent and type(intent2) is SellIntent and (agent2,intent2,agent1,intent1) not in usedIntentMatches):
                    exchanges.append(Exchange(agent2, agent1, intent1.money, intent1.commodities, intent1, intent2))
                    intent1.status = 'matched'
                    intent2.status = 'matched'
                    usedIntentMatches.append((agent2,intent2,agent1,intent1))

    #Exchanges happen here
    ##TODO: add some kind of randomization to order exchanges differently because of multiple agents ordering
    for exchange in exchanges:
        if(debug):
            print(str(exchange))
        primaryAgentHasCommodities = exchange.commoditiesFlow.issubset(exchange.primaryAgent.commodities)
        secondaryAgentHasMoney = exchange.secondaryAgent.money >= exchange.moneyFlow

        if primaryAgentHasCommodities and secondaryAgentHasMoney:
            exchange.primaryAgent.commodities -= exchange.commoditiesFlow
            exchange.secondaryAgent.commodities += exchange.commoditiesFlow
            exchange.primaryAgent.money += exchange.moneyFlow
            exchange.secondaryAgent.money -= exchange.moneyFlow

            exchange.buyIntent.status = 'completed'
            exchange.sellIntent.status = 'completed'
        else:
            if(not primaryAgentHasCommodities):
                exchange.buyIntent.status = 'unsufficient_commodities'
                exchange.sellIntent.status = 'unsufficient_commodities'

            if(not secondaryAgentHasMoney):
                exchange.buyIntent.status = 'unsufficient_money'
                exchange.sellIntent.status = 'unsufficient_money'
            

    #Next iteration
    time += 1
    sleep(sleepTime)
    if(interrupt):
        input()