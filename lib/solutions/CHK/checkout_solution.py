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
        for sku in skus:
            if sku not in self._combo_rules:
                self._combo_rules[sku] = {}

            self._combo_rules[sku] = {"Skus": set(skus) - set(sku), "Price": price, "Quantity": quantity}

    def __process_special_offers(self, sku, unit_price, offer_detail):
        for offer in offer_detail.split(', '):
            offer = offer.strip()
            if "buy any" in offer:
                elements = offer.split(" ")
                self.__add_combo_rule(elements[4][1:-1].split(','), int(elements[6]), int(elements[2]))
            elif "for" in offer:
                elements = offer.split(" ")
                self.__add_rule(elements[0][-1], int(elements[2]), int(elements[0][:-1]))
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

    @property
    def combo_rules(self):
        return OrderedDict(reversed(sorted(self._combo_rules.items())))


price_rules = PricingRules()
price_rules.initialize()

# skus = unicode string
def checkout(skus):
    return calculate_basket_cost(skus, True)


def calculate_basket_cost(skus, apply_discount):
    price = 0
    combo_price = 0
    basket = ''.join(sorted(skus))

    if apply_discount:
        for combo_rule in price_rules.combo_rules.items():
            found = 0
            if combo_rule[0] in basket:
                relevant_skus = set(combo_rule[0]).union(set(combo_rule[1]['Skus']))
                sku_prices = {}
                for sku in relevant_skus:
                    sku_price = price_rules.get_individual_item_price(sku)
                    if sku_price not in sku_prices:
                        sku_prices[sku_price] = set(sku)
                    else:
                        sku_prices[sku_price].add(sku)
                for sku in relevant_skus:
                    found += basket.count(sku)
                number_of_discounts = math.floor(found / int(combo_rule[1]['Quantity']))
                while number_of_discounts > 0:
                    removed = 0
                    combo_price += int(combo_rule[1]['Price'])
                    price_order = list(reversed(sorted(sku_prices.keys())))
                    while removed < int(combo_rule[1]['Quantity']):
                        for p in price_order:
                            for sku in sku_prices[p]:
                                if removed == int(combo_rule[1]['Quantity']):
                                    break
                                while sku in basket:
                                    basket = basket.replace(sku, '', 1)
                                    removed += 1
                                    if removed == int(combo_rule[1]['Quantity']):
                                        break
                    number_of_discounts -= 1

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

    return price + combo_price

