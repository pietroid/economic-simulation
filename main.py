from time import sleep
import copy
from multiset import *
from examples.basic_economy.setup import basicEconomyAgents
from examples.bank_company.setup import bankCompanyAgents
from examples.basic_bank.setup import basicBankAgents
from entities import BuyIntent, Exchange, SellIntent, get_description

##configs
sleepTime = 0.01
interrupt = True
debug = True

#choose what case example to simulate
#agents = basicEconomyAgents
#agents = bankCompanyAgents
agents = basicBankAgents

time = 1
exchanges = []
while(True):
    #Logging
    print(f'day #{time}')
    totalMoney = 0
    for agent in agents:
        print(
            f'{agent.__class__.__name__}'.ljust(15, ' ') +
            f'commodities: {list(get_description(agent.commodities).items())}'.ljust(100, ' ') +
            f'money: {agent.money}'
        )
        totalMoney += agent.money
    print(f'totalMoney: {totalMoney}')
    print()

    totalIntents = []
    messages = []
    #Transformations happen here
    for agent in agents:
        agent.iterate()

        #intents
        for intent in agent.intents:
            totalIntents.append((agent,intent))

        #capturing messages
        messages += agent.messagesToSend
        
    #distributing messages
    for message in messages:
        for agent in agents:
            if(agent.id == message.destinatary_id):
                agent.receivedMessages.append(message)
                break
        
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
               get_description(intent1.commodities) == get_description(intent2.commodities) and
               (intent1.target_id == None or intent1.target_id == agent2.id) and
               (intent2.target_id == None or intent2.target_id == agent1.id) ):

                if( type(intent1) is SellIntent and type(intent2) is BuyIntent and
                    intent1.money <= intent2.money and
                    (agent1,intent1,agent2,intent2) not in usedIntentMatches):

                    exchanges.append(Exchange(agent1, agent2, (intent1.money + intent2.money)/2, intent1.commodities, intent1, intent2))
                    intent1.add_status('matched', agent2.id)
                    intent2.add_status('matched', agent1.id)
                    usedIntentMatches.append((agent1,intent1,agent2,intent2))
                
                if( type(intent1) is BuyIntent and type(intent2) is SellIntent and
                    intent1.money >= intent2.money and
                    (agent2,intent2,agent1,intent1) not in usedIntentMatches):

                    exchanges.append(Exchange(agent2, agent1, (intent1.money + intent2.money)/2, intent1.commodities, intent2, intent1))
                    intent1.add_status('matched', agent2.id)
                    intent2.add_status('matched', agent1.id)
                    usedIntentMatches.append((agent2,intent2,agent1,intent1))

    #Exchanges happen here
    ##TODO: add some kind of randomization to order exchanges differently because of multiple agents ordering
    #TODO: add greedy exchanges (buy and sell as much as possible)
    for exchange in exchanges:
        primaryAgentHasCommodities = exchange.primaryAgent.contains(exchange.commoditiesFlow)
        secondaryAgentHasMoney = exchange.secondaryAgent.money >= exchange.moneyFlow
        belowBuyIntentLimit = exchange.buyIntent.completed_intents < exchange.buyIntent.exchanges_limit
        belowSellIntentLimit = exchange.sellIntent.completed_intents < exchange.sellIntent.exchanges_limit

        if (primaryAgentHasCommodities and 
           secondaryAgentHasMoney and 
           belowBuyIntentLimit and
           belowSellIntentLimit ):

            exchange.primaryAgent.remove(exchange.commoditiesFlow)
            for commodity in exchange.commoditiesFlow:
                commodity.last_agent_id = exchange.primaryAgent.id
            exchange.secondaryAgent.commodities += exchange.commoditiesFlow
            exchange.primaryAgent.money += exchange.moneyFlow
            exchange.secondaryAgent.money -= exchange.moneyFlow

            exchange.buyIntent.add_status('completed', exchange.primaryAgent.id)
            exchange.sellIntent.add_status('completed', exchange.secondaryAgent.id)
            
            exchange.buyIntent.completed_intents += 1
            exchange.sellIntent.completed_intents += 1
            if(debug):
                print(str(exchange))
        else:
            if(not primaryAgentHasCommodities):
                exchange.buyIntent.add_status('unsufficient_commodities',exchange.primaryAgent.id)
                exchange.sellIntent.add_status('unsufficient_commodities',exchange.secondaryAgent.id)

            if(not secondaryAgentHasMoney):
                exchange.buyIntent.add_status('unsufficient_money', exchange.primaryAgent.id)
                exchange.sellIntent.add_status('unsufficient_money', exchange.secondaryAgent.id)

            if(not belowBuyIntentLimit):
                exchange.buyIntent.add_status('limited_by_intent', exchange.primaryAgent.id)
                exchange.sellIntent.add_status('limited_by_intent', exchange.secondaryAgent.id)

            if(not belowSellIntentLimit):
                exchange.buyIntent.add_status('limited_by_intent', exchange.primaryAgent.id)
                exchange.sellIntent.add_status('limited_by_intent', exchange.secondaryAgent.id)
            

    #Next iteration
    time += 1
    sleep(sleepTime)
    if(interrupt):
        input()