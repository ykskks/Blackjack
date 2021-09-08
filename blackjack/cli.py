from blackjack.base import Dealer, Deck, Player
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
    dealer.draw(deck, display=False)

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
    pass
