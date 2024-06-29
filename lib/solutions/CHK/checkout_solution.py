# noinspection PyUnusedLocal
from collections import OrderedDict


class PricingRules(object):
    def __init__(self):
        self._rules = {}
        self._given_rules = '''
            | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |'''

    def __add_rule(self, item, price, quantity=1, free_item=''):
        if quantity not in self._rules:
            self._rules[quantity] = {}

        self._rules[quantity][item] = {"Price": price, "Free": free_item}

    def __process_special_offers(self, sku, unit_price, offer_detail):
        for offer in offer_detail.split(','):
            offer = offer.strip()
            if "buy any" in offer:
                here = True
            elif "for" in offer:
                self.__add_rule(offer[1], int(offer[7:]), int(offer[0]))
            elif "get one" in offer:
                if offer[11] == sku:
                    self.__add_rule(offer[1], unit_price * int(offer[0]), int(offer[0]) + 1)
                else:
                    self.__add_rule(offer[1], unit_price * int(offer[0]), int(offer[0]), offer[11])

    def initialize(self):
        for n, line in enumerate(self._given_rules[1:-1].split('\n')):
            values = [value.strip() for value in line.split('|')[1:-1]]
            sku = values[0]
            unit_price = int(values[1])
            self.__add_rule(values[0], int(values[1]))
            if len(values) > 2:
                offer_detail = values[2]
                if len(offer_detail) > 0:
                    self.__process_special_offers(sku, unit_price, offer_detail)

    def get_individual_item_price(self, item):
        return self.rules[1][item]['Price']

    @property
    def rules(self):
        return OrderedDict(reversed(sorted(self._rules.items())))


price_rules = PricingRules()
price_rules.initialize()


# price_rules = PricingRules()
# price_rules.add_rule('A', 50)
# price_rules.add_rule('B', 30)
# price_rules.add_rule('C', 20)
# price_rules.add_rule('D', 15)
# price_rules.add_rule('E', 40)
# price_rules.add_rule('F', 10)
# price_rules.add_rule('G', 20)
# price_rules.add_rule('H', 10)
# price_rules.add_rule('I', 35)
# price_rules.add_rule('J', 60)
# price_rules.add_rule('K', 70)
# price_rules.add_rule('L', 90)
# price_rules.add_rule('M', 15)
# price_rules.add_rule('N', 40)
# price_rules.add_rule('O', 10)
# price_rules.add_rule('P', 50)
# price_rules.add_rule('Q', 30)
# price_rules.add_rule('R', 50)
# price_rules.add_rule('S', 30)
# price_rules.add_rule('T', 20)
# price_rules.add_rule('U', 40)
# price_rules.add_rule('V', 50)
# price_rules.add_rule('W', 20)
# price_rules.add_rule('X', 90)
# price_rules.add_rule('Y', 10)
# price_rules.add_rule('Z', 50)
# price_rules.add_rule('A', 130, 3)
# price_rules.add_rule('A', 200, 5)
# price_rules.add_rule('B', 45, 2)
# price_rules.add_rule('E', 80, 2, 'B')
# price_rules.add_rule('F', 20, 3)
# price_rules.add_rule('H', 45, 5)
# price_rules.add_rule('H', 80, 10)
# price_rules.add_rule('K', 120, 2)
# price_rules.add_rule('N', 120, 3, 'M')
# price_rules.add_rule('P', 200, 5)
# price_rules.add_rule('Q', 80, 3)
# price_rules.add_rule('R', 150, 3, 'Q')
# price_rules.add_rule('U', 120, 4)
# price_rules.add_rule('V', 90, 2)
# price_rules.add_rule('V', 130, 3)

# skus = unicode string
def checkout(skus):
    return calculate_basket_cost(skus, True)


def calculate_basket_cost(skus, apply_discount):
    price = 0

    basket = ''.join(sorted(skus))
    updated_basket = basket
    discounted_items = ''

    for quantity, items in price_rules.rules.items():
        for item, item_details in items.items():
            item_pattern = item * quantity
            if item_pattern in basket:
                price += item_details['Price'] * basket.count(item_pattern)
                if apply_discount and item_details['Free'] != '':
                    if item_details['Free'] in updated_basket:
                        updated_basket = updated_basket.replace(item_details['Free'], '', basket.count(item_pattern))
                        discounted_items += item_details['Free'] * basket.count(item_pattern)
                basket = basket.replace(item_pattern, '')

    if len(basket) > 0:
        return -1

    if len(discounted_items) > 0:
        return calculate_basket_cost(updated_basket, False)

    return price

