from typing import List, Union, Type
from threading import Thread
from time import time
import numpy as np

from .player import Agent, User, LocalPlayer
from .blockchain import place_bets
from . import utils

class BlackjackGame:
    def __init__(self, players: List[Union[Type[Agent], User]], decks = 8):
        self.id = 3
        self.players = [LocalPlayer(p) for p in players]
        self.deck = np.array([[x if x < 11 else 10] * decks * 4 for x in range(1,14)]).flatten()
        np.random.shuffle(self.deck)
        self.cards = []
        self.total = 0
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
        try:
            self.collect_bets()
        except TimeoutError:
            raise TimeoutError
        
        for _ in range(2):
            for p in self.players:
                card, *self.deck = self.deck
                p.deal(card)
            card, *self.deck = self.deck
            self.cards.append(card)
        
        for p in self.players:
            while p.playing():
                match p.decision():
                    case "S":
                        pass
                    case "H":
                        card, *self.deck = self.deck
                        p.hit(card)
        
        while utils.compute_total(self.cards) < 17:
            card, *self.deck = self.deck
            self.cards.append(card)
            
        self.total = utils.compute_total(self.cards)

        print(f"Dealer ends on {self.total}")
        for p in self.players:
            match p.status():
                case 1:
                    print(f"Player {p} got blackjack on the deal")
                case 2:
                    print(f"Player {p} got blackjack after hitting")
                case 3:
                    print(f"Player {p} stood on {p.total}")
                case 4:
                    print(f"Player {p} busted")


        
# dq = agent.DeepQAgent()
# p = agent.ProbAgent()