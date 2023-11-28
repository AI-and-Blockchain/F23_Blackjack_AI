from model.game import BlackjackGame
from model.player import QAgent, WebUser
from model.utils import compute_total
import uvicorn
from sys import argv

class FrontendUser:
    def __init__(self):
        self.player = WebUser(input("Enter your name: ").strip(), 0, "wallet")
        self.game = BlackjackGame([self.player, QAgent()])
        self.playing = True
        self.bet()
        self.cards = []

    def bet(self):
        self.game.bet()
    
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
        
        ai = self.game.play_AI()
        for i, player in enumerate(ai):
            if len(player) == 0:
                print(f"AI {i + 1} stood.")
            else:
                print(f"AI {i + 1} hit {len(player)} time{'s'*(len(player) != 1)} and got {', '.join(map(str, player))}")
        dealer = self.game.play_dealer()
        if len(dealer) == 0:
            print("The dealer stood")
        else:
            print(f"The dealer hit {len(dealer)} time{'s'*(len(dealer) != 1)} and got {', '.join(map(str, dealer))}")
    
    def results(self):
        print("\n".join([x[0] for x in self.game.results()]))

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
        in_ = input("Press enter to begin:")
        if in_.lower() == "q":
            return
        f.run_game()
    


def web_test():
    try:
        port = int(argv[1])
    except:
        port = 8000
    uvicorn.run("frontend.app:app",host="localhost", port = port,reload=True)

if __name__ == "__main__":
    game_test()