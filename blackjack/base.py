import random
from typing import Callable

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

    def __repr__(self) -> str:
        return self.as_string

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

    @property
    def as_string(self) -> str:
        """このカードの文字列表現を取得する。

        Returns:
            str: カードの文字列表現
        """
        replace_patterns = {
            1: "A",
            11: "J",
            12: "Q",
            13: "K",
        }
        if self.__n in replace_patterns:
            return f"{self.__suit}_{replace_patterns[self.__n]}"

        return f"{self.__suit}_{self.__n}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, n) for suit in SUITS for n in NUMBERS]

    def shuffle(self) -> None:
        """デッキをシャッフルする。"""
        random.shuffle(self.cards)

    def pop(self) -> Card:
        """デッキの一番上（一番後ろ）のカードを取り出す。

        Returns:
            Card: 取り出されたカード
        """
        return self.cards.pop()


class Environment:
    """Agentの置かれた環境を表す。
    カードの数字は区別するが、スートは区別しない。
    順番は区別しない。
    相手と自分のカードは区別する。
    """

    def __init__(self, hands: list[Card], opponent_hands: list[Card]):
        self.hands = hands
        self.opponent_hands = opponent_hands

    def __eq__(self, other):
        # 自分のカードの数字と相手のカードの数字それぞれが集合として一致するとき
        # Agentの動作する環境が同値であるとみなす
        return (
            frozenset([c.n for c in self.hands]),
            frozenset([c.n for c in self.opponent_hands]),
        ) == (
            frozenset([c.n for c in other.hands]),
            frozenset([c.n for c in other.opponent_hands]),
        )

    def __hash__(self):
        # 自分のカードの数字の集合と相手のカードの数字の集合の組み合わせによりハッシュを計算する
        return hash(
            (
                frozenset([c.n for c in self.hands]),
                frozenset([c.n for c in self.opponent_hands]),
            )
        )


# TODO: enum.Enumを調べる
class Reward:
    win = 1
    lose = -1


class BasePlayer:
    def __init__(self):
        self.hands = []

    @property
    def total_points(self) -> int:
        """プレイヤーの現在の総ポイントを取得する。

        Returns:
            int: 総ポイント
        """
        return sum([card.point for card in self.hands])

    def draw(self, deck: Deck, display: bool = True) -> None:
        """デッキから一枚カードを引く。

        Args:
            deck (Deck): デッキ
        """
        if not isinstance(deck, Deck):
            raise TypeError("deck must be of type Deck.")

        new_card = deck.pop()
        self.hands.append(new_card)

        class_name = type(self).__name__

        if display:
            print(f"{class_name}は{new_card}を引きました。")
        else:
            print(f"{class_name}はカードを引きました。")


class Player(BasePlayer):
    def __init__(self, strategy: Callable):
        super().__init__()
        self.strategy = strategy

    def draw_again(self) -> bool:
        """もう一度デッキからカードを引くか選択する。

        Returns:
            bool: カードを引くかどうか
        """
        return self.strategy()


class Dealer(BasePlayer):
    def __init__(self):
        super().__init__()


class Agent(BasePlayer):
    def __init__(self):
        super().__init__()
        self.table = {}

    def accumulate_experience(self, env: Environment, reward: Reward) -> None:
        """ゲームをプレイすることにより経験を蓄積する。"""
        pass

    def _strategy(self) -> bool:
        """経験をもとにカードを引くかどうかの判断を行う。

        Returns:
            bool: カードを引くかどうか
        """
        pass

    def draw_again(self, env: Environment) -> bool:
        """もう一度デッキからカードを引くか選択する。

        Returns:
            bool: カードを引くかどうか
        """
        return self._strategy()
