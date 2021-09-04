import pytest

from blackjack.blackjack import Card, Dealer, Deck, Player


class TestCard:
    def test_init_suit_not_str(self):
        with pytest.raises(TypeError, match=r"suit must be of type.*"):
            Card(1, 5)  # type: ignore

    def test_init_suit_not_in_SUITS(self):
        with pytest.raises(ValueError, match=r"suit must be one of.*"):
            Card("A", 5)

    def test_init_n_not_int(self):
        with pytest.raises(TypeError, match=r"n must be of type.*"):
            Card("H", "5")  # type: ignore

    def test_init_n_not_in_NUMBERS(self):
        with pytest.raises(ValueError, match=r"n must be one of.*"):
            Card("H", 0)

    @pytest.mark.parametrize(
        "test_input,expected", [(("H", 3), 3), (("D", 10), 10), (("C", 13), 10)]
    )
    def test_point(self, test_input, expected):
        assert Card(*test_input).point == expected
