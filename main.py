from model.game import BlackjackGame
from model.player import QAgent, ProbAgent, WebUser
from model.utils import compute_total
import uvicorn

class FrontendUser:
    def __init__(self):
        self.player = WebUser(input("Enter your name: ").strip(), int(input("Enter your bet: ").strip()), input("Enter your wallet address: ").strip())
        self.game = BlackjackGame([self.player, QAgent()])
        self.playing = True
        self.bet()
        self.cards = []

    def bet(self):
        self.game.bet()
        print("Bets are locked in (not really)\nGame is ready")
    
    def reset(self):
        self.cards = []
        self.playing = True
        self.game.start()

    def deal(self):
        dealer, players = self.game.deal()
        if players[0][1] == 21:
            self.done = False
        self.cards = players[0][0]
        print(f"The dealer has been dealt two cards:\n\tFace up: {dealer[0]}\n\tFace down: {dealer[1]}")
        for i, p in enumerate(players):
            print(f"{self.player.id if i == 0 else 'Q Agent'} was dealt {' and '.join(map(str, p[0]))}. They have a hand total of {p[1]}")
    
    def decision(self):
        dec = input("Choose H for hit, or S for stand: ").upper()
        while dec not in ["H","S"]:
            dec = input("Choose H for hit, or S for stand: ").upper()
        return dec

    def play(self):
        while self.playing:
            choice = self.decision()
            card, self.playing = self.game.play_user(choice)
            if card != 0:
                self.cards.append(card)
                if self.playing:
                    print(f"{self.player.id} has been dealt a {card} and now has a hand total of {compute_total(self.cards)}")
                else:
                    print(f"{self.player.id} has been dealt a {card} and has busted with a hand total of {compute_total(self.cards)}")
            else:
                print(f"{self.player.id} has stood on {compute_total(self.cards)}")
        
        print(self.game.play_AI())
        print(self.game.play_dealer())
    
    def results(self):
        print(self.game.results())

    def run_game(self):
        self.reset()
        self.deal()
        self.play()
        self.results()

        

    

def game_test():
    # dq = QAgent()
    # u1 = User()
    # p = ProbAgent()

    f = FrontendUser()
    while True:
        input()
        f.run_game()
    


def web_test():
    port = input("Port: ")
    if port == "":
        port = 8000
    else:
        port = int(port)
    uvicorn.run("frontend.app:app",host="localhost", port = port,reload=True)

if __name__ == "__main__":
    web_test()