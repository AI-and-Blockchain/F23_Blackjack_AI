from typing import List, Union, Type

from .player import Agent, User

class BlackjackGame:
    def __init__(self, players: List[Union[Type[Agent], User]]):
        self.id = 3
        self.players = players
        print(self.players)

    def collect_bets(self):
        # collect bets from each player with some sort of member function
        # should we store these bets locally so that players cannot manipulate during the game?
        pass
# dq = agent.DeepQAgent()
# p = agent.ProbAgent()