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
        self.cards = [
            Card(suit, n) for suit in ["H", "D", "C", "S"] for n in range(1, 14)
        ]

    def shuffle(self) -> None:
        pass


class Player:
    pass


class Dealer:
    pass
