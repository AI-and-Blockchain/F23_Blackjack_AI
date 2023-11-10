from model.game import BlackjackGame
from model.player import QAgent, ProbAgent, User
import uvicorn

def game_test():
    # dq = QAgent()
    # u1 = User()
    # p = ProbAgent()

    g = BlackjackGame([User()])
    while True:
        try:
            g.run()
        except TimeoutError:
            print("User timed out")


def web_test():
    port = input("Port: ")
    if port == "":
        port = 8000
    else:
        port = int(port)
    uvicorn.run("frontend.app:app",host="localhost", port = port,reload=True)

if __name__ == "__main__":
    game_test()