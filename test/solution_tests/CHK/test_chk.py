from lib.solutions.CHK import checkout_solution


class TestCheckout():
    def test_simple_checkout(self):
        assert checkout_solution.checkout('ABC') == 100

    def test_single_item(self):
        assert checkout_solution.checkout('E') == 40

    def test_simple_offer(self):
        assert checkout_solution.checkout('AAAAAAAA') == 330

    def test_multiple_free_items(self):
        assert checkout_solution.checkout('EEEEBB') == 160

    def test_CHK_R2_027(self):
        assert checkout_solution.checkout('BEBEEE') == 160

    def test_CHK_R2_038(self):
        assert checkout_solution.checkout('ABCDEABCDE') == 280

    def test_simple_offers(self):
        assert checkout_solution.checkout('ABCABAD') == 210

    def test_complex_offers(self):
        assert checkout_solution.checkout('EAAAAAAAABBE') == 440

    def test_missed_f_offers(self):
        assert checkout_solution.checkout('FF') == 20

    def test_free_f(self):
        assert checkout_solution.checkout('FFF') == 20

    def test_multi_sku_offer(self):
        assert checkout_solution.checkout('STXYZ') == 82

    # - {"method": "checkout", "params": ["ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"],
    #    "id": "CHK_R5_147"}, expected: 1602, got: 1467
    # - {"method": "checkout", "params": ["LGCKAQXFOSKZGIWHNRNDITVBUUEOZXPYAVFDEPTBMQLYJRSMJCWH"],
    #    "id": "CHK_R5_148"}, expected: 1602, got: 1467
    # - {"method": "checkout", "params": ["AAAAAPPPPPUUUUEEBRRRQAAAHHHHHHHHHHKKVVVBBNNNMFFFQQQVVHHHHHSTX"],
    #    "id": "CHK_R5_149"}, expected: 1655, got: 1610

    #def test_CHK_R5_147(self):
    #    assert checkout_solution.checkout("ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ") == 1602

    def test_CHK_R5_140(self):
        assert checkout_solution.checkout("STXSTX") == 90

    def test_CHK_R5_141(self):
        assert checkout_solution.checkout("SSSZ") == 65

    def test_invalid_item(self):
        assert checkout_solution.checkout('AB1') == -1

    def test_lots_of_H(self):
        assert checkout_solution.checkout('HHHHHHHHHH') == 80


