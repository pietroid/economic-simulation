
from typing import List
from agents import Factory, Farmer, Land, Market, Miner, Mining, Worker
from entities import Exchange
from multiset import *
from commodities import *
## agents

agents = [
 land1,
 land2,
 farmer1,
 farmer2,
 worker1,
 worker2,
 miner1,
 miner2,
 factory,
 mining,
 market
] = [
    Land(),
    Land(),
    Farmer(),
    Farmer(),
    Worker(money=100),
    Worker(money=100),
    Miner(money=100),
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

exchanges: List[Exchange] = [
    #farmer with market
    Exchange(farmer1, market, 20, Multiset({food: 5})),
    Exchange(farmer2, market, 20, Multiset({food: 5})),

    #farmer with land
    Exchange(farmer1, land1, 0, Multiset({ farmerWork: 1, fertiliser:5 })),
    Exchange(farmer2, land2, 0, Multiset({ farmerWork: 1, fertiliser:5 })),
    Exchange(land1, farmer1, 0, Multiset({ food: 10 })),
    Exchange(land2, farmer2, 0, Multiset({ food: 10 })),
    
    #farmer with factory
    Exchange(factory, farmer1, 5, Multiset({ fertiliser: 4})),
    Exchange(factory, farmer2, 5, Multiset({ fertiliser: 4})),

    #worker with factory
    Exchange(worker1, factory, 20, Multiset({factoryWork: 1})),
    Exchange(worker2, factory, 20, Multiset({factoryWork: 1})),

    #worker with market
    Exchange(market, worker1, 3, Multiset({food: 1})),
    Exchange(market, worker2, 3, Multiset({food: 1})),

    #miner with mining
    Exchange(miner1, mining, 0, Multiset({minerWork})),
    Exchange(miner2, mining, 0, Multiset({minerWork})),
    Exchange(mining, miner1, 0, Multiset({minerals: 10})),
    Exchange(mining, miner2, 0, Multiset({minerals: 10})),

    #miner with factory
    Exchange(miner1, factory, 20, Multiset({minerals: 10})),
    Exchange(miner2, factory, 20, Multiset({minerals: 10})),

    #miner with market
    Exchange(market, miner1, 3, Multiset({food: 1})),
    Exchange(market, miner2, 3, Multiset({food: 1})),
]