from typing import List, Union, Type
from threading import Thread
from time import sleep
import numpy as np

from .player import Agent, User, LocalPlayer
import blockchain

class BlackjackGame:
    def __init__(self, players: List[Union[Type[Agent], User]], decks = 8):
        self.id = 3
        self.players = [LocalPlayer(p) for p in players]
        self.deck = np.array([[x] * decks * 4 for x in range(1,14)]).flatten()
        np.random.shuffle(self.deck)
        self.dealer_cards = []
        print(self.players)

    def collect_bets(self):
        threads = [Thread(target=p.place_bet()) for p in self.players]
        sleep(60)
        if any([t.is_alive() for t in threads]):
            raise TimeoutError
        blockchain.place_bets(self.players)


    def run(self):
        try:
            self.collect_bets()
        except TimeoutError:
            return "One of the users timed out on betting"
        
        for _ in range(2):
            for p in self.players:
                card, *self.deck = self.deck
                p.deal(card)
            card, *self.deck = self.deck
            self.dealer_cards.append(card)
             



        
# dq = agent.DeepQAgent()
# p = agent.ProbAgent()