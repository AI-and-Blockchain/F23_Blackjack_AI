import gym
import numpy as np

from collections import defaultdict
from tqdm import tqdm
from typing import Type, Tuple

from model.utils import compute_total
from model.q_table import Q_TABLE

class Agent: # Abstract Agent class, also found in CustomAgentExample.py
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"
    def __str__(self):
        return f"{self.id}"
    def add_card(self, card: int, total: int):
        raise Exception("Not yet implemented")
    def add_dealer_card(self, card: int):
        raise Exception("Not yet implemented")
    def decision(self) -> str:
        raise Exception("Not yet implemented")
    def start_new(self):
        raise Exception("Not yet implemented")

class QAgent(Agent):
    '''
    
    Original code provided by:
    
    # Author: Till Zemann
    # License: MIT License
    
    "Users of software using an MIT License are permitted to use, 
    copy, modify, merge publish, distribute, sublicense, and sell copies of the software."
    
    We modified this code to fit our own needs, and only some major important pieces remain.
    
    Link to original code: https://gymnasium.farama.org/tutorials/training_agents/blackjack_tutorial/
    
    '''
    def __init__(self, name: str="Pablo", smartness: float=0, trainable: bool=True):
        super().__init__()
        
        self.env = gym.make("Blackjack-v1", sab=True)
        
        self.trainable = trainable
        if self.trainable:
            learning_rate = 0.001
            initial_epsilon = 5
            final_epsilon = 0.01
            discount_factor = 0.95
            n_episodes = 5000
            
            self.lr = learning_rate
            self.discount_factor = discount_factor

            self.epsilon = initial_epsilon
            self.epsilon_decay = self.epsilon / (n_episodes / 2)
            
            self.episodes = n_episodes
            self.final_epsilon = final_epsilon

            self.training_error = []
        
        self.smart = True
        if smartness == 0:
            self.smart = False
        
        self.q_values = defaultdict(lambda: np.zeros(self.env.action_space.n))

        self.smartness = smartness
        if self.smart:
            self.q_values = Q_TABLE

        self.state = (0, 0, 0) # 
        
        self.id = name
        
    def get_action(self, obs: Tuple[int, int, bool], force: bool=True) -> int:
        """
        Returns the best action with probability (1 - epsilon)
        otherwise a random action with probability epsilon to ensure exploration.
        """
        # with probability (1 - smartness) return a random action to explore the environment
        if not force and np.random.random() >= self.smartness:
            return self.env.action_space.sample()

        # with probability smartness act "smart"
        else:
            return int(np.argmax(self.q_values[obs]))
        
    def update(self, obs: Tuple[int, int, bool], action: int, 
               reward: float, terminated: bool, next_obs: Tuple[int, int, bool]):
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
        
        if self.trainable:
        
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
        else:
            return
            
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
    
    def start_new(self):
        self.state = (0, 0, 0)

# dealer class that performs keeps track of its hand total and hits and stands in accordance with the rules
class Dealer(Agent):
    def __init__(self):
        self.id = "Dealer"
        self.cards = []
        self.total = 0
    
    def __repr__(self):
        return f"{self.id}"
    
    def add_card(self, card: int, total: int):
        self.cards.append(card)
        self.total = total

    def add_dealer_card(self, _):
        pass

    def decision(self) -> str:
        return "H" if self.total < 17 else "S"
    
    def start_new(self):
        self.cards = []
        self.total = 0

# the main agent that represents the frontend user
# nothing is required of it because it is all controlled through the frontend
class WebUser(Agent):
    def __init__(self, id, bet, address):
        self.id = id
        self.bet = bet
        self.address = address

    def __repr__(self):
        return f"{self.id}"
    
    def __str__(self):
        return f"{self.id}"

    def add_card(self, card: int, total: int):
        pass

    def add_dealer_card(self, card: int):
        pass
    
    def decision(self):
        pass
    
    def start_new(self):
        pass
    
# the class that wraps all Agent subclasses
# as it is defined by us for any Agent, it controls the main logic to ensure that numbers are not manipulated by malicious agent uploads
class LocalPlayer:
    def __init__(self, player: Type[Agent]):
        self.player = player
        self.cards = []
        self.dealer_card = 0
        self.total = 0
        self.done = 0 # 0 = playing, 1 = blackjack on first turn, 2 = blackjack after first, 3 = stood, 4 = bust

    def __str__(self):
        return str(self.player)

    def playing(self):
        return self.done == 0
    
    # adds the dealer's card to the local store and the player object
    def add_dealer_card(self, card: int):
        self.dealer_card = card
        self.player.add_dealer_card(card)

    # stores the dealt card and passes it to the player object
    def deal(self, card: int):
        self.cards.append(card)
        self.total = compute_total(self.cards)
        self.player.add_card(card, self.total)
        if len(self.cards) == 2 and self.total == 21:
            self.done = 1

    # requests a decision from the player object and sets an internal state
    def decision(self) -> str:
        d = self.player.decision()
        self.done = 3 if d == "S" else 0
        return d

    # sets the state
    def stand(self):
        self.done = 3
    
    # similar to deal, but has more state logic
    def hit(self, card: int):
        self.cards.append(card)
        self.total = compute_total(self.cards)
        self.player.add_card(card, self.total)
        if self.total == 21:
            self.done = 2
        elif self.total > 21:
            self.done = 4

    # returns the status
    def status(self) -> int:
        return self.done
    
    # resets the player object and its own variables
    def start_new(self):
        self.player.start_new()
        self.cards = []
        self.total = 0
        self.done = 0

# relic of testing the QAgent
if __name__ == "__main__":
    pablo = QAgent(smartness=1, trainable=False)