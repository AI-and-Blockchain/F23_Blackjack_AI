from typing import List, Union, Type


class Agent: # Abstract Agent class
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"

class DeepQAgent(Agent):
    def __init__(self):
        super().__init__()
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