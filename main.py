from model.game import BlackjackGame
from model.player import QAgent, ProbAgent, User


u1 = User()
dq = QAgent()
p = ProbAgent()

b = BlackjackGame(players=[u1, dq, p])
# dq = DeepQAgent()
# p = ProbAgent()