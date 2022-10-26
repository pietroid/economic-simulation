from time import sleep
from typing import List
from agents import Bank, Farmer, Land
from entities import Agent, Exchange
from multiset import *

time = 1
agents: List[Agent] = [Land(), Farmer(), Bank()]
exchanges: List[Exchange] = []

while(True):
    #Logging
    print(f'iteration #{time}')
    for agent in agents:
        print(f'name: {agent.__class__.__name__}, commodities: {agent.commodities}, money: {agent.money}')
    print()

    #Transformations happen here
    for agent in agents:
        agent.transform()

    #Exchanges happen here
    for exchange in exchanges:
        if exchange.commoditiesFlow.issubset(exchange.primaryAgent.commodities) and exchange.secondaryAgent.money >= exchange.moneyFlow:
            exchange.primaryAgent.commodities -= exchange.commoditiesFlow
            exchange.secondaryAgent.commodities += exchange.commoditiesFlow
            exchange.primaryAgent.money += exchange.moneyFlow
            exchange.secondaryAgent.money -= exchange.moneyFlow

    #Next iteration
    time += 1
    sleep(1)
