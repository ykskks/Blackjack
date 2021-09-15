import random

import pytest

from blackjack.base import (
    Action,
    Agent,
    BasePlayer,
    Card,
    Dealer,
    Deck,
    Environment,
    Player,
    Rank,
    Reward,
    Suit,
    Table,
)


class TestCard:
    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ((Suit.heart, Rank.three), 3),
            ((Suit.diamond, Rank.ten), 10),
            ((Suit.club, Rank.king), 10),
        ],
    )
    def test_point(self, test_input, expected):
        assert Card(*test_input).point == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [
            ((Suit.heart, Rank.three), "heart_3"),
            ((Suit.diamond, Rank.ten), "diamond_10"),
            ((Suit.club, Rank.king), "club_K"),
        ],
    )
    def test_as_string(self, test_input, expected):
        assert Card(*test_input).as_string == expected


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
        assert deck.pop() == Card(Suit.spade, Rank.king)
        assert deck.pop() == Card(Suit.spade, Rank.queen)


class TestEnvironment:
    def test_eq_true(self):
        assert Environment(
            [Card(Suit.spade, Rank.king), Card(Suit.diamond, Rank.five)],
            [Card(Suit.spade, Rank.ace), Card(Suit.heart, Rank.three)],
        ) == Environment(
            [Card(Suit.heart, Rank.five), Card(Suit.club, Rank.king)],
            [Card(Suit.diamond, Rank.three), Card(Suit.spade, Rank.ace)],
        )

    def test_eq_false(self):
        assert Environment(
            [Card(Suit.spade, Rank.king), Card(Suit.diamond, Rank.five)],
            [Card(Suit.spade, Rank.ace), Card(Suit.heart, Rank.three)],
        ) != Environment(
            [Card(Suit.diamond, Rank.king), Card(Suit.spade, Rank.five)],
            [Card(Suit.heart, Rank.three), Card(Suit.spade, Rank.two)],
        )

    def test_hash_true(self):
        assert hash(
            Environment(
                [Card(Suit.spade, Rank.king), Card(Suit.diamond, Rank.five)],
                [Card(Suit.spade, Rank.ace), Card(Suit.heart, Rank.three)],
            )
        ) == hash(
            Environment(
                [Card(Suit.heart, Rank.five), Card(Suit.club, Rank.king)],
                [Card(Suit.diamond, Rank.three), Card(Suit.spade, Rank.ace)],
            )
        )

    def test_hash_false(self):
        assert hash(
            Environment(
                [Card(Suit.spade, Rank.king), Card(Suit.diamond, Rank.five)],
                [Card(Suit.spade, Rank.ace), Card(Suit.heart, Rank.three)],
            )
        ) != hash(
            Environment(
                [Card(Suit.diamond, Rank.king), Card(Suit.spade, Rank.five)],
                [Card(Suit.heart, Rank.three), Card(Suit.spade, Rank.two)],
            )
        )


class TestBasePlayer:
    def test_total_points(self):
        player = BasePlayer()
        assert player.total_points == 0

        player.hands = [Card(Suit.heart, Rank.five), Card(Suit.spade, Rank.queen)]
        assert player.total_points == 15

    def test_draw(self):
        deck = Deck()
        player = BasePlayer()

        player.draw(deck)
        assert player.hands == [Card(Suit.spade, Rank.king)]

        player.draw(deck)
        assert player.hands == [
            Card(Suit.spade, Rank.king),
            Card(Suit.spade, Rank.queen),
        ]


class TestPlayer:
    def test_draw_displayed_class_name(self, capsys):
        deck = Deck()
        player = Player(lambda: False)
        player.draw(deck)
        captured = capsys.readouterr()
        assert "Player" in captured.out

    def test_draw_again(self):
        player = Player(lambda: False)
        assert not player.draw_again()

        player = Player(lambda: True)
        assert player.draw_again()


class TestDealer:
    def test_draw_displayed_class_name(self, capsys):
        deck = Deck()
        dealer = Dealer()
        dealer.draw(deck)
        captured = capsys.readouterr()
        assert "Dealer" in captured.out


@pytest.fixture
def env():
    return Environment(
        [Card(Suit.spade, Rank.two), Card(Suit.spade, Rank.queen)],
        [Card(Suit.heart, Rank.four)],
    )


@pytest.fixture
def env_swapped():
    return Environment(
        [Card(Suit.spade, Rank.queen), Card(Suit.spade, Rank.two)],
        [Card(Suit.heart, Rank.four)],
    )


@pytest.fixture
def envs():
    return [
        Environment(
            [Card(Suit.spade, Rank.two), Card(Suit.spade, Rank.queen)],
            [Card(Suit.heart, Rank.four)],
        ),
        Environment(
            [
                Card(Suit.spade, Rank.two),
                Card(Suit.spade, Rank.queen),
                Card(Suit.diamond, Rank.ace),
            ],
            [Card(Suit.heart, Rank.four)],
        ),
    ]


@pytest.fixture
def actions():
    return [Action.draw, Action.stand]


class TestTable:
    def test_update_single(self, envs, actions):
        table = Table()

        table.update(envs, actions, Reward.win)

        for env, action in zip(envs, actions):
            assert table[env][action] == 1

    def test_update_multiple(self, envs, actions):
        table = Table()

        table.update(envs, actions, Reward.win)
        table.update(envs, actions, Reward.tie)
        table.update(envs, actions, Reward.win)
        table.update(envs, actions, Reward.lose)

        for env, action in zip(envs, actions):
            assert table[env][action] == (1 + 0 + 1 - 1) / 4

    def test_different_environment_with_same_key(self, env, env_swapped):
        table = Table()

        table._table[env][Action.draw] = 1.0
        assert table._table[env_swapped][Action.draw] == 1.0

        table._table[env_swapped][Action.draw] += 1.0
        assert table._table[env][Action.draw] == 2.0

    def test_different_environment_with_same_total_points(self, env):
        table = Table()
        env_same_total_points = Environment(
            [Card(Suit.spade, Rank.two), Card(Suit.spade, Rank.king)],
            [Card(Suit.heart, Rank.four)],
        )

        table._table[env][Action.draw] = 1.0
        assert table._table[env_same_total_points][Action.draw] != 1.0

        table._table[env_same_total_points][Action.draw] = -1.0
        assert table._table[env][Action.draw] != -1.0


class TestAgent:
    def test_strategy_one_is_better(self, envs, actions):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.win)
        agent.register_experience(envs, actions, Reward.tie)
        agent.register_experience(envs, actions, Reward.win)

        for env, action in zip(envs, actions):
            # 一方のActionの評価値が高い場合は常にそちらが選ばれる
            assert agent._strategy(env) == action

    def test_strategy_random_draw(self, envs, actions, monkeypatch):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.tie)

        # 両方のActionの評価値が等しい場合にはランダムに選ばれる
        # random.uniform() > 0.Rank.fiveならdraw
        monkeypatch.setattr(random, "random", lambda: 0.7)
        for env in envs:
            assert agent._strategy(env) == Action.draw

    def test_strategy_random_stand(self, envs, actions, monkeypatch):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.tie)

        # 両方のActionの評価値が等しい場合にはランダムに選ばれる
        # random.uniform() <= 0.Rank.fiveならstand
        monkeypatch.setattr(random, "random", lambda: 0.2)
        for env in envs:
            assert agent._strategy(env) == Action.stand

    def test_draw_again_one_is_better(self, envs, actions):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.win)
        agent.register_experience(envs, actions, Reward.tie)
        agent.register_experience(envs, actions, Reward.win)

        assert agent.draw_again(envs[0])
        assert not agent.draw_again(envs[1])

    def test_draw_again_random_draw(self, envs, actions, monkeypatch):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.tie)

        # 両方のActionの評価値が等しい場合にはランダムに選ばれる
        # random.uniform() > 0.Rank.fiveならdraw
        monkeypatch.setattr(random, "random", lambda: 0.7)
        for env in envs:
            assert agent.draw_again(env)

    def test_draw_again_random_stand(self, envs, actions, monkeypatch):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.tie)

        # 両方のActionの評価値が等しい場合にはランダムに選ばれる
        # random.uniform() <= 0.Rank.fiveならstand
        monkeypatch.setattr(random, "random", lambda: 0.2)
        for env in envs:
            assert not agent.draw_again(env)
