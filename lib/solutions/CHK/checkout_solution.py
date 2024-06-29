

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}

    total = 0
    basket = skus.split()
    for sku in basket:
        try:
            total += prices[sku]
        except:
            return -1

    return total




