# noinspection PyUnusedLocal
from collections import OrderedDict
import math


class PricingRules:
    def __init__(self):
        self._rules = {}
        self._combo_rules = {}

    def __add_rule(self, item, price, quantity=1, free_item=''):
        if quantity not in self._rules:
            self._rules[quantity] = {}

        self._rules[quantity][item] = {"Price": price, "Free": free_item}

    def __add_combo_rule(self, skus, price, quantity):
        if skus not in self._combo_rules:
            self._combo_rules[skus] = {}
            self._combo_rules[skus] = {"Price": price, "Quantity": quantity}

    def __process_special_offers(self, sku, unit_price, offer_detail):
        for offer in offer_detail.split(', '):
            offer = offer.strip()
            if "buy any" in offer:
                parts = offer.split(" ")
                self.__add_combo_rule(parts[4][1:-1].replace(',',''), int(parts[6]), int(parts[2]))
            elif "for" in offer:
                parts = offer.split(" ")
                self.__add_rule(parts[0][-1], int(parts[2]), int(parts[0][:-1]))
            elif "get one" in offer:
                if offer[11] == sku:
                    self.__add_rule(offer[1], unit_price * int(offer[0]), int(offer[0]) + 1)
                else:
                    self.__add_rule(offer[1], unit_price * int(offer[0]), int(offer[0]), offer[11])

    def load_rules(self, rules):
        for line in rules.strip().split('\n'):
            values = [value.strip() for value in line.split('|')[1:-1]]
            sku = values[0]
            unit_price = int(values[1])
            self.__add_rule(sku, unit_price)
            if len(values) > 2:
                offer_detail = values[2]
                if offer_detail:
                    self.__process_special_offers(sku, unit_price, offer_detail)

    def get_individual_item_price(self, item):
        return self.rules[1][item]['Price']

    @property
    def rules(self):
        return OrderedDict(reversed(sorted(self._rules.items())))

    @property
    def combo_rules(self):
        return OrderedDict(reversed(sorted(self._combo_rules.items())))


class Checkout:
    def __init__(self, pricing_rules):
        self._pricing_rules = pricing_rules
        self._basket = {}

    def __validate_basket(self):
        valid_items = []
        for quantity, item in self._pricing_rules.rules.items():
            valid_items.append(item)
        return True

    def calculate_basket_cost(self, skus, apply_discount=True):
        price = 0
        combo_price = 0
        self._basket = ''.join(sorted(skus))

        if not self.__validate_basket():
            return -1

        if apply_discount:
            for skus, combo_rule in self._pricing_rules.combo_rules.items():
                found = sum(self._basket.count(s) for s in skus)
                number_of_discounts = math.floor(found / combo_rule['Quantity'])
                combo_price += combo_rule['Price'] * number_of_discounts
                to_remove = number_of_discounts * combo_rule['Quantity']
                discounted_items = []
                for sku in skus:
                    discounted_items.append(tuple((sku, self._pricing_rules.get_individual_item_price(sku))))
                discounted_items = sorted(discounted_items, key=lambda x: x[1], reverse=True)
                while to_remove > 0:
                    for sku in discounted_items:
                        while sku[0] in self._basket and to_remove > 0:
                            self._basket = self._basket.replace(sku[0], '', 1)
                            to_remove -= 1

        updated_basket = self._basket
        discounted_items = ''

        for quantity, items in self._pricing_rules.rules.items():
            for item, item_details in items.items():
                item_pattern = item * quantity
                while item_pattern in self._basket:
                    price += item_details['Price']
                    if apply_discount and item_details['Free']:
                        if item_details['Free'] in updated_basket:
                            updated_basket = updated_basket.replace(item_details['Free'], '', 1)
                            discounted_items += item_details['Free']
                    self._basket = self._basket.replace(item_pattern, '', 1)

        for item in self._basket:
            price += self._pricing_rules.get_individual_item_price(item)

        if discounted_items:
            return self.calculate_basket_cost(updated_basket, False) + combo_price

        return price + combo_price


# skus = unicode string
def checkout(skus):

    rules='''
        | A    | 50    | 3A for 130, 5A for 200          |
        | B    | 30    | 2B for 45                       |
        | C    | 20    |                                 |
        | D    | 15    |                                 |
        | E    | 40    | 2E get one B free               |
        | F    | 10    | 2F get one F free               |
        | G    | 20    |                                 |
        | H    | 10    | 5H for 45, 10H for 80           |
        | I    | 35    |                                 |
        | J    | 60    |                                 |
        | K    | 70    | 2K for 120                      |
        | L    | 90    |                                 |
        | M    | 15    |                                 |
        | N    | 40    | 3N get one M free               |
        | O    | 10    |                                 |
        | P    | 50    | 5P for 200                      |
        | Q    | 30    | 3Q for 80                       |
        | R    | 50    | 3R get one Q free               |
        | S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | U    | 40    | 3U get one U free               |
        | V    | 50    | 2V for 90, 3V for 130           |
        | W    | 20    |                                 |
        | X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
        | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |
    '''

    pricing_rules = PricingRules()
    pricing_rules.load_rules(rules)

    checkout_solution = Checkout(pricing_rules)
    return checkout_solution.calculate_basket_cost(skus)

