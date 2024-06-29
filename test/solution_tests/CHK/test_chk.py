from lib.solutions.CHK import checkout_solution


class TestCheckout():
    def test_simple_checkout(self):
        assert checkout_solution.checkout('ABC') == 100

    def test_simple_offers(self):
        assert checkout_solution.checkout('ABCABAD') == 210

    def test_complex_offers(self):
        assert checkout_solution.checkout('EAAAAAAAABBE') == 425

    def test_invalid_item(self):
        assert checkout_solution.checkout('ABF') == -1

