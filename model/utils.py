convert = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:10, 12:10, 13:10}

def compute_total(cards):
    total = 0
    for card in sorted(list(map(lambda x: convert[x], cards)), reverse=True):
        if card == 1 and 21 - total >= 11:
            total += 11
        else:
            total += card
    return total