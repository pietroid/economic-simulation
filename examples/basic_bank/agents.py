from entities import Agent
from multiset import Multiset as m

class Bank(Agent):
    def __init__(self):
        super().__init__(100, m({}))
    
    def transform(self):
        print(self.id)
        pass

class Person(Agent):
    def __init__(self):
        super().__init__(0, m({}))

    def transform(self):
        print(self.id)
        pass