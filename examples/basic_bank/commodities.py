from entities import C

class Debt(C):
    def __init__(self):
        super().__init__('debt of $100')
        self.interest = 1
        self.daysToExpiration = 10
        self.status = 'active'

debt = lambda : Debt()
bread = lambda: C('1kg of bread')
wood = lambda: C('5kg of wood')
wheat = lambda: C('1kg of wheat')
workForce = lambda: C('1 day of work')
artifact = lambda: C('complex artifact')