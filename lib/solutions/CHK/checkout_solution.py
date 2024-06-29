# noinspection PyUnusedLocal
from collections import OrderedDict

class PricingRules(object):
    def __init__(self):
        self._rules = {}

    def add_rule(self, item, price, quantity=1, free_item=''):
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
    price_rules.add_rule('E', 40)
    price_rules.add_rule('A', 130, 3)
    price_rules.add_rule('B', 45, 2)
    price_rules.add_rule('A', 200, 5)
    price_rules.add_rule('E', 40, 2, 'B')

    price = 0

    basket = ''.join(sorted(skus))

    for quantity, items in price_rules.rules.items():
        for item, item_price in items.items():
            item_pattern = item * quantity
            if item_pattern in basket:
                price += item_price * basket.count(item_pattern)
                basket = basket.replace(item_pattern, '')

    if len(basket) > 0:
        return -1

    return price

