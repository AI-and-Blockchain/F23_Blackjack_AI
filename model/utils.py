from enum import Enum
from typing import List

# Converts deck numbers to point values
convert = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:10, 12:10, 13:10}

# enumeration to have variable representations of states
class States(Enum):
    PLAYERS = 0
    BET = 1
    READY = 2
    DEAL = 3
    PLAY = 4
    AI = 5
    DEALER = 6
    RESULTS = 7

# computes the total of a deck of cards
def compute_total(cards: List[int]) -> int:
    total = 0
    for card in sorted(list(map(lambda x: convert[x], cards)), reverse=True):
        if card == 1 and 21 - total >= 11:
            total += 11
        else:
            total += card
    return total