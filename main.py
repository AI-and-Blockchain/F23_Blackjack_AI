from model.game import BlackjackGame
from model.player import DeepQAgent, ProbAgent, User


u1 = User()
dq = DeepQAgent()
p = ProbAgent()

b = BlackjackGame(players=[u1, dq, p])
# dq = DeepQAgent()
# p = ProbAgent()