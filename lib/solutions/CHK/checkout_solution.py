# noinspection PyUnusedLocal
from collections import OrderedDict

class PricingRules(object):
    def __init__(self):
        self._rules = {}

    def add_rule(self, item, price, quantity=1):
        if quantity not in self._rules:
            self._rules[quantity] = {}

        self._rules[quantity][item] = price

    @property
    def rules(self):
        return OrderedDict(reversed(sorted(self._rules.items())))

# skus = unicode string
def checkout(skus):
    price_rules = PricingRules()
    price_rules.add_rule('A', 50)
    price_rules.add_rule('B', 30)
    price_rules.add_rule('C', 20)
    price_rules.add_rule('D', 15)
    price_rules.add_rule('A', 130, 3)
    price_rules.add_rule('B', 45, 2)

    for quantity, item in price_rules.rules.items():
        for sku in skus:




