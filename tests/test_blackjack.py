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
    Reward,
    Table,
)


class TestCard:
    def test_init_suit_not_str(self):
        with pytest.raises(TypeError, match=r"suit must be of type.*"):
            Card(1, 5)  # type: ignore

    def test_init_suit_not_in_SUITS(self):
        with pytest.raises(ValueError, match=r"suit must be one of.*"):
            Card("A", 5)

    def test_init_rank_not_int(self):
        with pytest.raises(TypeError, match=r"rank must be of type.*"):
            Card("H", "5")  # type: ignore

    def test_init_rank_not_in_RANKS(self):
        with pytest.raises(ValueError, match=r"rank must be one of.*"):
            Card("H", 0)

    @pytest.mark.parametrize(
        "test_input,expected", [(("H", 3), 3), (("D", 10), 10), (("C", 13), 10)]
    )
    def test_point(self, test_input, expected):
        assert Card(*test_input).point == expected

    @pytest.mark.parametrize(
        "test_input,expected",
        [(("H", 3), "H_3"), (("D", 10), "D_10"), (("C", 13), "C_K")],
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
        assert deck.pop() == Card("S", 13)
        assert deck.pop() == Card("S", 12)


class TestEnvironment:
    def test_eq_true(self):
        assert Environment(
            [Card("S", 13), Card("D", 5)], [Card("S", 1), Card("H", 3)]
        ) == Environment([Card("H", 5), Card("C", 13)], [Card("D", 3), Card("S", 1)])

    def test_eq_false(self):
        assert Environment(
            [Card("S", 13), Card("D", 5)], [Card("S", 1), Card("H", 3)]
        ) != Environment([Card("D", 13), Card("S", 5)], [Card("H", 3), Card("S", 2)])

    def test_hash_true(self):
        assert hash(
            Environment([Card("S", 13), Card("D", 5)], [Card("S", 1), Card("H", 3)])
        ) == hash(
            Environment([Card("H", 5), Card("C", 13)], [Card("D", 3), Card("S", 1)])
        )

    def test_hash_false(self):
        assert hash(
            Environment([Card("S", 13), Card("D", 5)], [Card("S", 1), Card("H", 3)])
        ) != hash(
            Environment([Card("D", 13), Card("S", 5)], [Card("H", 3), Card("S", 2)])
        )


class TestBasePlayer:
    def test_total_points(self):
        player = BasePlayer()
        assert player.total_points == 0

        player.hands = [Card("H", 5), Card("S", 12)]
        assert player.total_points == 15

    def test_draw(self):
        deck = Deck()
        player = BasePlayer()

        player.draw(deck)
        assert player.hands == [Card("S", 13)]

        player.draw(deck)
        assert player.hands == [Card("S", 13), Card("S", 12)]


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
def envs():
    return [
        Environment([Card("S", 2), Card("S", 12)], [Card("H", 4)]),
        Environment([Card("S", 2), Card("S", 12), Card("D", 1)], [Card("H", 4)]),
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
        # random.uniform() > 0.5ならdraw
        monkeypatch.setattr(random, "random", lambda: 0.7)
        for env in envs:
            assert agent._strategy(env) == Action.draw

    def test_strategy_random_stand(self, envs, actions, monkeypatch):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.tie)

        # 両方のActionの評価値が等しい場合にはランダムに選ばれる
        # random.uniform() <= 0.5ならstand
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
        # random.uniform() > 0.5ならdraw
        monkeypatch.setattr(random, "random", lambda: 0.7)
        for env in envs:
            assert agent.draw_again(env)

    def test_draw_again_random_stand(self, envs, actions, monkeypatch):
        agent = Agent()

        agent.register_experience(envs, actions, Reward.tie)

        # 両方のActionの評価値が等しい場合にはランダムに選ばれる
        # random.uniform() <= 0.5ならstand
        monkeypatch.setattr(random, "random", lambda: 0.2)
        for env in envs:
            assert not agent.draw_again(env)
