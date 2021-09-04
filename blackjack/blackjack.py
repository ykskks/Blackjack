import random

SUITS = ("H", "D", "C", "S")
NUMBERS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)


class Card:
    def __init__(self, suit: str, n: int):
        if not isinstance(suit, str):
            raise TypeError("suit must be of type str.")
        elif suit not in SUITS:
            raise ValueError(f"suit must be one of {SUITS}.")
        self.__suit = suit

        if not isinstance(n, int):
            raise TypeError("n must be of type int.")
        elif n not in NUMBERS:
            raise ValueError(f"n must be one of {NUMBERS}.")
        self.__n = n

    def __eq__(self, other):
        return (self.__suit, self.__n) == (other.__suit, other.__n)

    def __hash__(self):
        return hash((self.__suit, self.__n))

    @property
    def suit(self):
        return self.__suit

    @property
    def n(self):
        return self.__n

    @property
    def point(self) -> int:
        """このカードのポイントを取得する。

        Returns:
            int: カードのポイント
        """
        return min(self.__n, 10)


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
        if not isinstance(deck, Deck):
            raise TypeError("deck must be of type Deck.")

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
        if not isinstance(deck, Deck):
            raise TypeError("deck must be of type Deck.")

        if not isinstance(display, bool):
            raise TypeError("display must be of type bool.")

        new_card = deck.pop()
        self.hands.append(new_card)
        if display:
            print(f"Dealerは{new_card}を引きました。")
        else:
            print("Dealerはカードを引きました。")
