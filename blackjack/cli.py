from .blackjack import Dealer, Deck, Player


def draw_again():
    return input("もう一回引きますか？ y/n") == "y"


def execute():
    deck = Deck()
    player = Player()
    dealer = Dealer()

    deck.shuffle()

    player.draw(deck)
    dealer.draw(deck)

    player.draw(deck)
    dealer.draw(deck, display=False)

    while True:
        player.draw(deck)

        if player.total_points > 21:
            break

        if not draw_again():
            break

    while dealer.total_points < 17:
        dealer.draw(deck)

    if dealer.total_points > player.total_points:
        print("Dealerの勝ちです。")
    elif dealer.total_points < player.total_points:
        print("Plaeyrの勝ちです。")
    else:
        print("引き分けです。")
