from tqdm import tqdm

from blackjack.base import Action, Agent, Dealer, Deck, Environment, Player, Reward
from blackjack.strategy import ALLOWED_STRATEGIES, input_strategy, random_strategy


def play():
    over = False

    input_ = input(f"Choose player strategy. {ALLOWED_STRATEGIES} > ")

    while input_ not in ALLOWED_STRATEGIES:
        input_ = input(
            f"Allowed strategies are {ALLOWED_STRATEGIES}, but given {input_}. Please choose again. > "
        )

    if input_ == "random":
        player_strategy = random_strategy
    else:
        player_strategy = input_strategy

    deck = Deck()
    player = Player(player_strategy)
    dealer = Dealer()

    deck.shuffle()

    player.draw(deck)
    dealer.draw(deck)

    player.draw(deck)
    dealer.draw(deck, display_card=False)

    while True:
        print(f"現在の総ポイントは{player.total_points}です。")
        if not player.draw_again():
            break

        player.draw(deck)

        if player.total_points > 21:
            print("Dealerの勝ちです。")
            over = True
            break

    if not over:

        while dealer.total_points < 17:
            dealer.draw(deck)

            if dealer.total_points > 21:
                print("Playerの勝ちです。")
                over = True
                break

    if not over:

        if dealer.total_points > player.total_points:
            print("Dealerの勝ちです。")
        elif dealer.total_points < player.total_points:
            print("Playerの勝ちです。")
        else:
            print("引き分けです。")


def train():
    num_plays_train = 1000
    num_plays_test = 1000
    agent = Agent()

    for _ in tqdm(range(num_plays_train), desc="Training..."):
        over = False
        deck = Deck()
        dealer = Dealer()
        agent.reset_hands()
        envs = []
        actions = []

        deck.shuffle()

        agent.draw(deck, verbose=False)
        dealer.draw(deck, verbose=False)

        agent.draw(deck, verbose=False)
        dealer.draw(deck, verbose=False)

        # dealerの2枚目はagentには見えない
        envs.append(Environment(agent.hands, dealer.hands[:-1]))

        while True:
            if not agent.draw_again(envs[-1]):
                actions.append(Action.stand)
                break

            agent.draw(deck, verbose=False)
            actions.append(Action.draw)

            if agent.total_points > 21:
                over = True
                agent.register_experience(envs, actions, Reward.lose)
                break

            envs.append(Environment(agent.hands, dealer.hands[:-1]))

        if not over:

            while dealer.total_points < 17:
                dealer.draw(deck, verbose=False)

                if dealer.total_points > 21:
                    over = True
                    agent.register_experience(envs, actions, Reward.win)
                    break

        if not over:

            if dealer.total_points > agent.total_points:
                agent.register_experience(envs, actions, Reward.lose)
            elif dealer.total_points < agent.total_points:
                agent.register_experience(envs, actions, Reward.win)
            else:
                agent.register_experience(envs, actions, Reward.tie)

    agent.table.show()

    win_count = 0
    for _ in tqdm(range(num_plays_test), desc="Testing..."):
        over = False
        deck = Deck()
        dealer = Dealer()
        agent.reset_hands()
        envs = []

        deck.shuffle()

        agent.draw(deck, verbose=False)
        dealer.draw(deck, verbose=False)

        agent.draw(deck, verbose=False)
        dealer.draw(deck, verbose=False)

        envs.append(Environment(agent.hands, dealer.hands[:-1]))

        while True:
            if not agent.draw_again(envs[-1]):
                break

            agent.draw(deck, verbose=False)

            if agent.total_points > 21:
                over = True
                break

            envs.append(Environment(agent.hands, dealer.hands[:-1]))

        if not over:

            while dealer.total_points < 17:
                dealer.draw(deck, verbose=False)

                if dealer.total_points > 21:
                    over = True
                    win_count += 1
                    break

        if not over:

            if dealer.total_points > agent.total_points:
                pass
            elif dealer.total_points < agent.total_points:
                win_count += 1
            else:
                pass

    print(f"Agentの勝率: {win_count / num_plays_test:.3f}")
