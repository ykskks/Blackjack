import pytest

from blackjack.base import Card, Deck, Player


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


class TestDeck:
    def test_len_cards(self):
        assert len(Deck().cards) == 52

    def test_shuffle(self):
        deck = Deck()
        cards_original = deck.cards.copy()

        deck.shuffle()
        cards_shuffled = deck.cards.copy()

        assert set(cards_original) == set(cards_shuffled)
        assert cards_original != cards_shuffled

    def test_pop(self):
        deck = Deck()
        assert deck.pop() == Card("S", 13)
        assert deck.pop() == Card("S", 12)


class TestPlayer:
    def test_total_points(self):
        player = Player(lambda x: False)
        assert player.total_points == 0

        player.hands = [Card("H", 5), Card("S", 12)]
        assert player.total_points == 15

    def test_draw(self):
        deck = Deck()
        player = Player(lambda x: False)

        player.draw(deck)
        assert player.hands == [Card("S", 13)]

        player.draw(deck)
        assert player.hands == [Card("S", 13), Card("S", 12)]
