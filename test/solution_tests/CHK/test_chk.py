from lib.solutions.CHK import checkout_solution


class TestCheckout():
    def test_simple_checkout(self):
        assert checkout_solution.checkout('A B C') == 100

    def test_invalid_item(self):
        assert checkout_solution.checkout('A B E') == -1


