import gym
import numpy as np
import pandas as pd

from collections import defaultdict
from tqdm import tqdm
from typing import List, Union, Type

from model.utils import compute_total
from model.q_table import Q_TABLE

class Agent: # Abstract Agent class
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"
    def __str__(self):
        return f"{self.id}"
    def add_card(self, card):
        pass
    def add_dealer_card(self, card):
        pass
    def decision(self):
        """
        Returns "S" for stand and "H" for hit
        """
        pass
    def start_new(self):
        pass

class QAgent(Agent):
    def __init__(self, learning_rate: float=0.001, initial_epsilon: float=5, 
                 final_epsilon: float=0.01, discount_factor: float=0.95, 
                 n_episodes: int=5000, smart: bool=True):
        super().__init__()
        
        self.env = gym.make("Blackjack-v1", sab=True)
        
        self.q_values = defaultdict(lambda: np.zeros(self.env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = self.epsilon / (n_episodes / 2)
        
        self.episodes = n_episodes
        self.final_epsilon = final_epsilon

        self.training_error = []
        # self.Q = np.zeros(shape=(self.env.observation_space.shape, self.env.action_space.shape))
        # print(self.Q)
        self.smart = smart
        if self.smart:
            self.q_values = Q_TABLE
            
        self.state = (0, 0, 0) # 
        
        self.id = 1
        
    def get_action(self, obs: tuple[int, int, bool], force: bool=True) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability epsilon return a random action to explore the environment
        if not force and np.random.random() < self.epsilon:
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
        
    def train(self):
        
        env = gym.wrappers.RecordEpisodeStatistics(self.env, deque_size=self.episodes)
        
        for episode in tqdm(range(self.episodes)):
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
            
    def decision(self) -> str:
        decisions = {0: "S", 1: "H"}
        return decisions[self.get_action(self.state, force=True)] # obs: (player's sum, dealer's card, usable ace)
    
    def add_card(self, card: int, _):

        if card == 1:
            if self.state[0] + 11 <= 21:
                self.state = (self.state[0] + 11, self.state[1], 1)
            else:
                self.state = (self.state[0] + 1, self.state[1], 0)
        else:
            
            if self.state[2] and self.state[0] + card > 21:
                self.state = (self.state[0] - 10 + card, self.state[1], 0)
            else: # either bust or usable ace
                self.state = (self.state[0] + card, self.state[1], self.state[2])
    
    def add_dealer_card(self, card: int):
        
        self.state = (self.state[0], card, self.state[2])
        
        
            
class ProbAgent(Agent):
    def __init__(self):
        super().__init__()
        self.id = 2
        
# class User(Agent):
#     def __init__(self, id):
#         self.id = id
#         self.cards = []
#         self.dealer_card = 0
#         self.total = 0
#     def __repr__(self):
#         return f"{self.id}"
#     def place_bet(self) -> float:
#         return float(input("Enter how much you would like to bet: "))

#     def add_card(self, card, total):
#         self.cards.append(card)
#         self.total = total
#         print(f"You have been dealt a {card}. Your cards are: {', '.join(map(str, self.cards))}. Your hand total is {self.total}. {f'The dealer has a {self.dealer_card}.' if self.dealer_card != 0 else ''}")

    # def add_dealer_card(self, card):
    #     self.dealer_card = card
    #     print(f"The dealer has been dealt a {card}")

#     def decision(self):
#         dec = input("Choose H for hit, or S for stand: ").upper()
#         while dec not in ["H","S"]:
#             dec = input("Choose H for hit, or S for stand: ").upper()
#         return dec
    
#     def start_new(self):
#         self.cards = []
#         self.total = 0
        
class Dealer(Agent):
    def __init__(self):
        self.id = "Dealer"
        self.cards = []
        self.total = 0
    
    def __repr__(self):
        return f"{self.id}"
    
    def add_card(self, card, total):
        self.cards.append(card)
        self.total = total

    def decision(self):
        return "H" if self.total < 17 else "S"
    
    def start_new(self):
        self.cards = []
        self.total = 0

class WebUser(Agent):
    def __init__(self, id, bet, address):
        self.id = id
        self.bet = bet
        self.address = address

    def __repr__(self):
        return f"{self.id}"
    
    def __str__(self):
        return f"{self.id}"

    def add_card(self, card, total):
        pass

    def add_dealer_card(self, card):
        pass
    
    def decision(self):
        pass
    
    def start_new(self):
        self.cards = []
        self.total = 0
    

class LocalPlayer:
    def __init__(self, player: Type[Agent]):
        self.player = player
        self.cards = []
        self.dealer_card = 0
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
    
    def add_dealer_card(self, card: int):
        self.dealer_card = card
        self.player.add_dealer_card(card)

    def deal(self, card: int):
        self.cards.append(card)
        self.total = compute_total(self.cards)
        self.player.add_card(card, self.total)
        if len(self.cards) == 2 and self.total == 21:
            self.done = 1

    def decision(self):
        d = self.player.decision()
        self.done = 3 if d == "S" else 0
        return d

    def stand(self):
        self.done = 3
    
    def hit(self, card: int):
        self.cards.append(card)
        self.total = compute_total(self.cards)
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

if __name__ == "__main__":
    
    pablo = QAgent()