from blackjack import Dealer, Deck, Player


def draw_again():
    return input("もう一回引きますか？ y/n") == "y"


def execute():
    over = False

    deck = Deck()
    player = Player()
    dealer = Dealer()

    deck.shuffle()

    player.draw(deck)
    dealer.draw(deck)

    player.draw(deck)
    dealer.draw(deck, display=False)

    while True:
        if not draw_again():
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


if __name__ == "__main__":
    execute()
