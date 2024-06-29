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
        return self._rules



# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}

    total = 0
    basket = skus.split()
    for sku in basket:
        try:
            if (item[])
            total += prices[sku]
        except:
            return -1

    return total





