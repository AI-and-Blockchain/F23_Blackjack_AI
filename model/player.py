import gym
import numpy as np
import pandas as pd

from collections import defaultdict
from tqdm import tqdm
from typing import List, Union, Type
from . import utils

class Agent: # Abstract Agent class
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"
    def __str__(self):
        return f"{self.id}"
    def place_bet(self) -> float:
        pass
    def add_card(self, card):
        pass
    def decision(self):
        """
        Returns "S" for stand and "H" for hit
        """
        pass
    def start_new(self):
        pass

class QAgent(Agent):
    def __init__(self, learning_rate: float, initial_epsilon: float, 
                 epsilon_decay: float, final_epsilon: float, discount_factor: float=0.95, smart: bool=True):
        super().__init__()
        
        self.env = gym.make("Blackjack-v1", sab=True)
        
        self.q_values = defaultdict(lambda: np.zeros(self.env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []
        # self.Q = np.zeros(shape=(self.env.observation_space.shape, self.env.action_space.shape))
        # print(self.Q)
        self.smart = smart
        self.id = 1
        
    def get_action(self, obs: tuple[int, int, bool]) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment
        if np.random.random() < self.epsilon:
            return self.env.action_space.sample()

        # with probability (1 - epsilon) act greedily (exploit)
        else:
            return int(np.argmax(self.q_values[obs]))
        
    def update(self, obs: tuple[int, int, bool], action: int, 
               reward: float, terminated: bool, next_obs: tuple[int, int, bool]):
        """Updates the Q-value of an action."""
        future_q_value = (not terminated) * np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_value - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference
        )
        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
        self.epsilon = max(self.final_epsilon, self.epsilon - self.epsilon_decay)
        
    def train(self, episodes: int):
        
        env = gym.wrappers.RecordEpisodeStatistics(self.env, deque_size=episodes)
        
        for episode in tqdm(range(episodes)):
            obs, info = env.reset()
            done = False

            # play one episode
            while not done:
                action = self.get_action(obs)
                # print(action)
                next_obs, reward, terminated, truncated, info = env.step(action)

                # update the agent
                self.update(obs, action, reward, terminated, next_obs)

                # update if the environment is done and the current obs
                done = terminated or truncated
                obs = next_obs

            self.decay_epsilon()
            
        def get_action(self, obs: tuple[int, int, bool]):
            # assuming q table is full (not learning from moves anymore)
            
            if self.smart:
                # action = self.get_action(obs)
                return self.get_action(obs) # 0 is stand, 1 is hit
            else:
                pass
            
class ProbAgent(Agent):
    def __init__(self):
        super().__init__()
        self.id = 2
        
class User(Agent):
    def __init__(self):
        self.id = input("Enter a username: ")
        self.cards = []
        self.total = 0
    def __repr__(self):
        return f"{self.id}"
    def place_bet(self) -> float:
        return float(input("Enter how much you would like to bet: "))

    def add_card(self, card, total):
        self.cards.append(card)
        self.total = total
        print(f"You have been dealt a {card}. Your cards are: {', '.join(map(str, self.cards))}. Your hand total is {self.total}.")

    def decision(self):
        dec = input("Choose H for hit, or S for stand: ").upper()
        while dec not in ["H","S"]:
            dec = input("Choose H for hit, or S for stand: ").upper()
        return dec
    
    def start_new(self):
        self.cards = []
        self.total = 0
        
class Dealer(Agent):
    def __init__(self):
        self.id = "Dealer"
        self.cards = []
        self.total = 0
    
    def __repr__(self):
        return f"{self.id}"
    
    def place_bet(self) -> float:
        return 0.0

    def add_card(self, card, total):
        self.cards.append(card)
        self.total = total

    def decision(self):
        return "H" if self.total < 17 else "S"
    
    def start_new(self):
        self.cards = []
        self.total = 0

    

class LocalPlayer:
    def __init__(self, player: Union[Type[Agent], User]):
        self.player = player
        self.bet = 0
        self.cards = []
        self.total = 0
        self.done = 0 # 0 = playing, 1 = blackjack on first turn, 2 = blackjack after first, 3 = stood, 4 = bust

    def __str__(self):
        return str(self.player)

    def blackjack(self, cards, total: int) -> bool:
        for i, card in enumerate(cards):
            if card == 1:
                return self.blackjack(cards[i+1:], total + 1) or self.blackjack(cards[i+1:], total + 11)
            else:
                total += card
        if total == 21:
            return True
        else:
            return False

    def playing(self):
        return self.done == 0

    def place_bet(self):
        self.bet = self.player.place_bet()

    def get_bet(self) -> float:
        return float(self.bet)
    
    def deal(self, card: int):
        self.cards.append(card)
        self.total = utils.compute_total(self.cards)
        self.player.add_card(card, self.total)
        if len(self.cards) == 2 and self.total == 21:
            self.done = 1

    def decision(self):
        d = self.player.decision()
        self.done = 3 if d == "S" else 0
        return d
    
    def hit(self, card: int):
        self.cards.append(card)
        self.total = utils.compute_total(self.cards)
        self.player.add_card(card, self.total)
        if self.total == 21:
            self.done = 2
        elif self.total > 21:
            self.done = 4

    def status(self):
        return self.done
    
    def start_new(self):
        self.player.start_new()
        self.cards = []
        self.total = 0
        self.done = 0
        self.bet = 0

if __name__ == "__main__":
    from random import randint
    p = LocalPlayer(User())
    print(p.blackjack([10,1],0))
    p.deal(1)
    p.deal(9)
    p.hit(1)
    while p.playing():
        match p.decision():
            case "S":
                pass
            case "H":
                p.hit(randint(1,13))
    print(p.status())
    
    pablo = QAgent()