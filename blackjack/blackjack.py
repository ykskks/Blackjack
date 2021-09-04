import random

SUITS = ("H", "D", "C", "S")
NUMBERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)


class Card:
    def __init__(self, suit: str, n: int):
        self._suit = suit
        self._n = n

    @property
    def point(self) -> int:
        """このカードのポイントを取得する。

        Returns:
            int: カードのポイント
        """
        return min(self._n, 10)


class Deck:
    def __init__(self):
        self.cards = [Card(suit, n) for suit in SUITS for n in NUMBERS]

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def pop(self) -> Card:
        return self.cards.pop()


class Player:
    def __init__(self):
        self.hands = []

    @property
    def total_points(self) -> int:
        return sum([card.point for card in self.hands])

    def draw(self, deck: Deck) -> None:
        new_card = deck.pop()
        self.hands.append(new_card)
        print(f"Playerは{new_card}を引きました。")


class Dealer:
    def __init__(self):
        self.hands = []

    @property
    def total_points(self) -> int:
        return sum([card.point for card in self.hands])

    def draw(self, deck: Deck, display: bool = True) -> None:
        new_card = deck.pop()
        self.hands.append(new_card)
        if display:
            print(f"Dealerは{new_card}を引きました。")
        else:
            print("Dealerはカードを引きました。")
