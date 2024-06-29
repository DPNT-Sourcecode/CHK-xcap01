from lib.solutions.CHK import checkout_solution


class TestCheckout():
    def test_simple_checkout(self):
        assert checkout_solution.checkout('ABC') == 100

    def test_single_item(self):
        assert checkout_solution.checkout('E') == 40

    def test_multiple_free_items(self):
        assert checkout_solution.checkout('EEEEBB') == 160

    def test_CHK_R2_027(self):
        assert checkout_solution.checkout('BEBEEE') == 160

    def test_CHK_R2_038(self):
        assert checkout_solution.checkout('ABCDEABCDE') == 280

    def test_simple_offers(self):
        assert checkout_solution.checkout('ABCABAD') == 210

    def test_complex_offers(self):
        assert checkout_solution.checkout('EAAAAAAAABBE') == 425

    def test_invalid_item(self):
        assert checkout_solution.checkout('ABF') == -1

