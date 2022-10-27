from time import sleep
from multiset import *
from data import exchanges
from agents import *
from data import agents

time = 1

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
    sleep(0.01)
