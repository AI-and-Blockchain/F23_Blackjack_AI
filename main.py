from model.game import BlackjackGame
from model.player import QAgent, ProbAgent, User


dq = QAgent()
# u1 = User()
# p = ProbAgent()

g = BlackjackGame([User()])
try:
    g.run()
except TimeoutError:
    print("User timed out")