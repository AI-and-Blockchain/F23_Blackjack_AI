from typing import List, Union, Type
from threading import Thread
from time import sleep
from random import shuffle, randint
import numpy as np

from .player import Agent, User
import blockchain
from .localplayer import LocalPlayer

class BlackjackGame:
    def __init__(self, players: List[Union[Type[Agent], User]], decks = 8):
        self.id = 3
        self.players = [LocalPlayer(p) for p in players]
        self.deck = np.array([[x] * decks * 4 for x in range(1,14)]).flatten()
        print(self.players)

    def collect_bets(self):
        threads = [Thread(target=p.place_bet()) for p in self.players]
        sleep(60)
        if any([t.is_alive() for t in threads]):
            raise Exception("One of the users timed out")
        blockchain.place_bets(self.players, [p.get_bet() for p in self.players])


    def run(self):
        self.collect_bets()


        pass
# dq = agent.DeepQAgent()
# p = agent.ProbAgent()