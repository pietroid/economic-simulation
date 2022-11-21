from examples.basic_economy.agents import Factory, Farmer, Land, Market, Miner, Mining, Worker
from entities import Exchange
from multiset import Multiset as m
from examples.basic_economy.commodities import *
## agents

basicEconomyAgents = [
    Land(),
    Farmer(commodities = m({fertiliser() :1000})),
    Worker(money=100),
    Miner(money=100),
    Factory(money=1000),
    Mining(),
    Market(money=1000)
]

### commodities flow
##           farmer <- factory
## Market <- farmer <-> land

## Factory <- worker <- Market

## Factory <- miner <-> mining
##            miner <- Market

## exchanges
# A $<--- B
# A --->c B 

"""
exchanges: List[Exchange] = [
    #farmer with market
    Exchange(farmer1, market, 20, m({food: 5})),
    Exchange(farmer2, market, 20, m({food: 5})),

    #farmer with land
    Exchange(farmer1, land1, 0, m({ farmerWork: 1, fertiliser:5 })),
    Exchange(farmer2, land2, 0, m({ farmerWork: 1, fertiliser:5 })),
    Exchange(land1, farmer1, 0, m({ food: 10 })),
    Exchange(land2, farmer2, 0, m({ food: 10 })),
    
    #farmer with factory
    Exchange(factory, farmer1, 5, m({ fertiliser: 4})),
    Exchange(factory, farmer2, 5, m({ fertiliser: 4})),

    #worker with factory
    Exchange(worker1, factory, 20, m({factoryWork: 1})),
    Exchange(worker2, factory, 20, m({factoryWork: 1})),

    #worker with market
    Exchange(market, worker1, 3, m({food: 1})),
    Exchange(market, worker2, 3, m({food: 1})),

    #miner with mining
    Exchange(miner1, mining, 0, m({minerWork})),
    Exchange(miner2, mining, 0, m({minerWork})),
    Exchange(mining, miner1, 0, m({minerals: 10})),
    Exchange(mining, miner2, 0, m({minerals: 10})),

    #miner with factory
    Exchange(miner1, factory, 10, m({minerals: 10})),
    Exchange(miner2, factory, 10, m({minerals: 10})),

    #miner with market
    Exchange(market, miner1, 3, m({food: 1})),
    Exchange(market, miner2, 3, m({food: 1})),
]
"""