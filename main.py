from typing import List
from entities import Agent, Exchange

agents: List[Agent] = []
exchanges: List[Exchange] = []

def iteration():
    #Transformations happen here
    for i in range(0,len(agents)):
        initialAgent = agents[i]
        finalAgent = initialAgent.transform()
        agents[i] = finalAgent

    #Exchanges happen here
    for exchange in exchanges:
        #TODO: test this condition
        if exchange.primaryAgent.commodities.intersection(exchange.commoditiesFlow) == exchange.commoditiesFlow and exchange.secondaryAgent.money >= exchange.moneyFlow :
            exchange.primaryAgent.commodities -= exchange.commoditiesFlow
            exchange.secondaryAgent.commodities += exchange.commoditiesFlow
            exchange.primaryAgent.money += exchange.moneyFlow
            exchange.secondaryAgent.money -= exchange.moneyFlow