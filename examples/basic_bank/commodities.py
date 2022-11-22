from entities import C

class Debt(C):
    def __init__(self):
        super().__init__('debt of $100')
        self.interest = 1
        self.daysToExpiration = 10
        self.status = 'active'

debt = lambda : Debt()