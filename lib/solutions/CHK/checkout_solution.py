

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    prices = []
    prices.append('A', 50, True)
    prices.append('B', 30, True)
    prices.append('C', 20, False)
    prices.append('D', 15, False)

    total = 0
    basket = skus.split()
    for sku in basket:



