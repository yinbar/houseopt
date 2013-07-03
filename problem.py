from .util import shuffled

class House:
    def __init__(self, name, count):
        self.count = count
        self.name = name
        self.customers = set()

    def add(self, customer):
        self.customers.append(customer.name)

    def add_to_problem(self, lp):
        lp.add_dependent_variable(('HOUSE', self.name),
            {(customer, self.name): 1 for customer in self.customers},
            0, self.count)

class Customer:
    def __init__(self, name):
        self.name = name
        self.customers = {}
        self.houses = {}

    def add(self, house, preference):
        if house.name in self.houses:
            raise ValueError('Customer {!r} has 2 preferences for house {!r}'.
                             format(self.name, house.name))
        self.houses[house.name] = preference

    def add_to_problem(self, lp):
        for house, pref in shuffled(self.houses.items()):
            lp.add_binary_variable((self.name, house), pref)
        
        lp.add_dependent_variable(('CUSTOMER', self.name),
            {(self.name, house): 1 for house in self.houses},
            0, 1)

class HousingProblem:
    def __init__(self):
        self.houses = {}
        self.customers = {}

    def add_house(self, name, count):
        if name in self.houses:
            raise ValueError('Doubly declared house name {!r}'.format(name))

        self.houses[name] = House(name, count)

    def add_customer(self, name, preferences):
        if name in self.customers:
            raise ValueError('Duplicate customer name {!r}'.format(name))

        cust = Customer(name)
        self.customers[cust.name] = cust

        for house,pref in preferences.items():
            if house not in houses:
                raise ValueError('Unknown house type {!r}'.format(houses))

            if pref != 0:
                houses[house].add(cust)
                cust.add(houses[house], pref)

    def add_to_problem(self, lp):
        for customer in customers:
            customer.add_to_problem(lp)

        for house in houses:
            house.add_to_problem(lp)
