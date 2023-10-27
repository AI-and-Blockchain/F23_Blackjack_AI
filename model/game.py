from typing import List, Union, Type

from .player import Agent, User

class BlackjackGame:
    def __init__(self, players: List[Union[Type[Agent], User]]):
        self.id = 3
        self.players = players
        print(self.players)
# dq = agent.DeepQAgent()
# p = agent.ProbAgent()