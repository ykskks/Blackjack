from .blackjack import Dealer, Deck, Player


def execute():
    deck = Deck()
    player = Player()
    dealer = Dealer()
    print(deck, player, dealer)
