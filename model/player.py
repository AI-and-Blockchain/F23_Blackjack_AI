import numpy as np
import pandas as pd
import gym

from typing import List, Union, Type




class Agent: # Abstract Agent class
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"

class QAgent(Agent):
    def __init__(self):
        super().__init__()

        # self.Q = np.zeros(shape=(self.env.observation_space.shape, self.env.action_space.shape))
        # print(self.Q)
        self.id = 1
        
        
        
    
    
class ProbAgent(Agent):
    def __init__(self):
        super().__init__()
        self.id = 2
        
class User:
    def __init__(self):
        self.id = 3
    def __repr__(self):
        return f"{self.id}"
    

class LocalPlayer:
    def __init__(self, player: Union[Type[Agent], User]):
        self.player = player
        self.bet = 0
        self.cards = []

    def place_bet(self):
        self.bet = self.player.place_bet()

    def get_bet(self) -> float:
        return float(self.bet)
    
    def deal(self, card: int):
        self.cards.append(card)
        
        
if __name__ == "__main__":
    pablo = QAgent()