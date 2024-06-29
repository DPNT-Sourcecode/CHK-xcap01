# noinspection PyUnusedLocal
from collections import OrderedDict


class PricingRules(object):
    def __init__(self):
        self._rules = {}

    def add_rule(self, item, price, quantity=1, free_item=''):
        if quantity not in self._rules:
            self._rules[quantity] = {}

        self._rules[quantity][item] = {"Price": price, "Free": free_item}

    def get_individual_item_price(self, item):
        return self.rules[1][item]['Price']

    @property
    def rules(self):
        return OrderedDict(reversed(sorted(self._rules.items())))

price_rules = PricingRules()
price_rules.add_rule('E', 80, 2, 'B')
price_rules.add_rule('B', 30)
price_rules.add_rule('C', 20)
price_rules.add_rule('D', 15)
price_rules.add_rule('A', 50)
price_rules.add_rule('E', 40)
price_rules.add_rule('A', 130, 3)
price_rules.add_rule('B', 45, 2)
price_rules.add_rule('A', 200, 5)

# skus = unicode string
def checkout(skus):

    price = 0
    total_discounts = 0

    basket = ''.join(sorted(skus))
    original_basket = basket
    discounted_items = ''

    for quantity, items in price_rules.rules.items():
        for item, item_details in items.items():
            item_pattern = item * quantity
            if item_pattern in basket:
                price += item_details['Price'] * basket.count(item_pattern)
                if item_details['Free'] != '':
                    if item_details['Free'] in original_basket:
                        total_discounts = price_rules.get_individual_item_price(item_details['Free'])
                        original_basket = original_basket.replace(item_details['Free'], '', 1)
                        discounted_items += item_details['Free']
                basket = basket.replace(item_pattern, '')

    if len(basket) > 0:
        return -1

    return price


