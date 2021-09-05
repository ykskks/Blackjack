import random

ALLOWED_STRATEGIES = ("random", "input")


def random_strategy() -> bool:
    return random.random() < 0.5


def input_strategy() -> bool:
    return input("もう一回引きますか？ [y/n]") == "y"
