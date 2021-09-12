import enum
import random
from collections import defaultdict
from typing import Callable


class Suit(enum.Enum):
    heart = enum.auto()
    diamond = enum.auto()
    club = enum.auto()
    spade = enum.auto()


class Rank(enum.IntEnum):
    ace = 1
    two = 2
    three = 3
    four = 4
    five = 5
    six = 6
    seven = 7
    eight = 8
    nine = 9
    ten = 10
    jack = 11
    queen = 12
    king = 13


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.__suit = suit
        self.__rank = rank

    def __eq__(self, other):
        return (self.__suit, self.__rank) == (other.__suit, other.__rank)

    def __hash__(self):
        return hash((self.__suit, self.__rank))

    def __repr__(self) -> str:
        return self.as_string

    @property
    def suit(self):
        return self.__suit

    @property
    def rank(self):
        return self.__rank

    @property
    def point(self) -> int:
        """このカードのポイントを取得する。

        Returns:
            int: カードのポイント
        """
        return min(self.__rank, 10)

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
        if self.__rank in replace_patterns:
            return f"{self.__suit.name}_{replace_patterns[self.__rank]}"

        return f"{self.__suit.name}_{self.__rank}"


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]

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
        # 自分のカードのランクと相手のカードのランクそれぞれが集合として一致するとき
        # Agentの動作する環境が同値であるとみなす
        return (
            frozenset([c.rank for c in self.hands]),
            frozenset([c.rank for c in self.opponent_hands]),
        ) == (
            frozenset([c.rank for c in other.hands]),
            frozenset([c.rank for c in other.opponent_hands]),
        )

    def __hash__(self):
        # 自分のカードのランクの集合と相手のカードのランクの集合の組み合わせによりハッシュを計算する
        return hash(
            (
                frozenset([c.rank for c in self.hands]),
                frozenset([c.rank for c in self.opponent_hands]),
            )
        )


class Action(enum.Enum):
    draw = enum.auto()
    stand = enum.auto()


class Reward(enum.IntEnum):
    win = 1
    tie = 0
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


class Table:
    """あるEnvironmentにおけるActionの評価値を保存する。
    過去のEnvironmentとActionペアに関する全Rewardを平均したものが、
    現在の評価値となる。
    """

    def __init__(self):
        # 全てのEnvironment, Actionペアに対してゼロで初期化する
        # ref: https://stackoverflow.com/questions/5029934/defaultdict-of-defaultdict
        self._table = defaultdict(lambda: defaultdict(float))
        self._count = defaultdict(lambda: defaultdict(int))

    def update(
        self, envs: list[Environment], actions: list[Action], reward: Reward
    ) -> None:
        for env, action in zip(envs, actions):
            old_value = self._table[env][action]
            old_count = self._count[env][action]
            # 同一のEnvironmentとActionのペアに関して全期間のRewardの平均をとる
            self._table[env][action] = (old_value * old_count + reward.value) / (
                old_count + 1
            )
            self._count[env][action] += 1

    def __getitem__(self, key) -> defaultdict[Action, float]:
        return self._table[key]


class Agent(BasePlayer):
    def __init__(self):
        super().__init__()
        self.table = Table()

    def register_experience(
        self, envs: list[Environment], actions: list[Action], reward: Reward
    ) -> None:
        """勝敗決定時にそれまでにAgentがとったEnvironmentと
        Actionのペアに対してRewardを割り当ててTableを更新する。
        """
        self.table.update(envs, actions, reward)

    def _strategy(self, env: Environment) -> Action:
        """過去のRewardをもとに、このEnvironmentに対する
        Rewardの平均値が高いActionを返す。

        Args:
            env (Environment): Agentの置かれた環境

        Returns:
            Action: Rewardの平均値が高いAction
        """
        scores = self.table[env]

        # Actionの評価値が同じ場合はランダムに選ぶ
        if scores[Action.draw] == scores[Action.stand]:
            if random.random() > 0.5:
                return Action.draw
            else:
                return Action.stand

        # 最大のvalueをもつkeyを返す
        return max(scores, key=scores.get)  # type: ignore

    def draw_again(self, env: Environment) -> bool:
        """もう一度デッキからカードを引くか選択する。

        Returns:
            bool: カードを引くかどうか
        """
        selected_action = self._strategy(env)
        return selected_action == Action.draw
