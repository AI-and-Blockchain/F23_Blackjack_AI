from typing import List, Union, Type
from threading import Thread
from time import time
import numpy as np

from .player import Agent, User, Dealer, LocalPlayer
from .blockchain import place_bets
from . import utils

class BlackjackGame:
    def __init__(self, players: List[Union[Type[Agent], User]], decks = 8):
        self.id = 3
        self.dealer = LocalPlayer(Dealer())
        self.players = [LocalPlayer(p) for p in players]
        self.deck = np.array([[x if x < 11 else 10] * decks * 4 for x in range(1,14)]).flatten()
        np.random.shuffle(self.deck)
        
        print(self.players)

    def collect_bets(self):
        threads = [Thread(target=p.place_bet) for p in self.players]
        for t in threads:
            t.start()
        start = time()
        while time() - start < 60 and any([t.is_alive() for t in threads]):
            pass
        if any([t.is_alive() for t in threads]):
            raise TimeoutError
        place_bets(self.players)


    def run(self):
        self.dealer.start_new()
        for p in self.players:
            p.start_new()
        try:
            self.collect_bets()
        except TimeoutError:
            raise TimeoutError
        
        for _ in range(2):
            for p in self.players:
                card, *self.deck = self.deck
                p.deal(card)
            card, *self.deck = self.deck
            self.dealer.deal(card)
        
        for p in self.players:
            while p.playing():
                match p.decision():
                    case "S":
                        pass
                    case "H":
                        card, *self.deck = self.deck
                        p.hit(card)
        
        while self.dealer.playing():
            match self.dealer.decision():
                case "S":
                    pass
                case "H":
                    card, *self.deck = self.deck
                    self.dealer.hit(card)

        dealer_status = self.dealer.status()
        dealer_total = self.dealer.total
        for p in self.players:
            match p.status():
                case 1:
                    if dealer_status == 1:
                        print(f"Both the dealer and player {p} got a natural blackjack, they push.")
                    else:
                        print(f"Player {p} got a natural blackjack and wins {p.bet * 3}.")
                case 2:
                    if dealer_status == 1:
                        print(f"The dealer had natural blackjack, {p} loses.")
                    elif dealer_status == 2:
                        print(f"Both the dealer and player {p} got a blackjack, they push.")
                    else:
                        print(f"Player {p} got blackjack after hitting and wins {p.bet * 2}")
                case 3:
                    match dealer_status:
                        case 1:
                            print(f"The dealer had natural blackjack, player {p} loses.")
                        case 2:
                            print(f"The dealer got a blackjack, player {p} loses.")
                        case 3:
                            print(f"Player {p} stood on {p.total} and the dealer stood on {dealer_total},", end = '')
                            if p.total > dealer_total:
                                print(f" {p} wins {p.bet * 2}.")
                            elif p.total < dealer_total:
                                print(f" {p} loses.")
                            else:
                                print(f" they push.")
                        case 4:
                            print(f"Player {p} stood on {p.total} and the dealer busted, {p} wins {p.bet * 2}.")
                case 4:
                    print(f"Player {p} busted and lost.")


        
# dq = agent.DeepQAgent()
# p = agent.ProbAgent()