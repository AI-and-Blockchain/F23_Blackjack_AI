from typing import List, Type
import numpy as np

from model.player import Agent, Dealer, LocalPlayer
from model.utils import States

class BlackjackGame:
    def __init__(self, players: List[Type[Agent]] = [], decks = 8):
        self.id = 3
        self.dealer = LocalPlayer(Dealer())
        self.deck = np.array([[x if x < 11 else 10] * decks * 4 for x in range(1,14)]).flatten()
        np.random.shuffle(self.deck)
        if len(players) == 0:
            self.state = States.PLAYERS
        else:
            self.players = [LocalPlayer(p) for p in players]
            self.state = States.BET
        # print(self.players)
    
    def revert(self):
        self.__init__()

    def add_players(self, players: List[Type[Agent]]):
        if self.state != States.PLAYERS:
            return
        self.players = [LocalPlayer(p) for p in players]
        self.state = States.BET

    def bet(self):
        if self.state != States.BET:
            return
        self.state = States.READY


    def start(self):
        if self.state != States.READY:
            return
        self.dealer.start_new()
        for p in self.players:
            p.start_new()
        self.state = States.DEAL
        

    def deal(self):
        if self.state != States.DEAL:
            return ([], [])
        for i in range(2):
            for p in self.players:
                card, *self.deck = self.deck
                p.deal(card)
            card, *self.deck = self.deck
            self.dealer.deal(card)
            if i == 0:
                for p in self.players:
                    p.add_dealer_card(card)
        self.state = States.PLAY
        return [int(card) for card in self.dealer.cards], [[[int(card) for card in p.cards], p.total] for p in self.players]
    
    def play_user(self, decision):
        if self.state != States.PLAY:
            return 0, True
        p = self.players[0]
        if not p.playing():
            self.state = States.AI
            return 0, False
        match decision:
            case "S":
                p.stand()
                card = 0
            case "H":
                card, *self.deck = self.deck
                p.hit(card)
        if p.playing():
            return int(card), True
        else:
            self.state = States.AI
            return int(card), False
    
    def play_AI(self):
        if self.state != States.AI:
            return []
        all_cards = []
        for p in self.players[1:]:
            cards = []
            while p.playing():
                match p.decision():
                    case "S":
                        pass
                    case "H":
                        card, *self.deck = self.deck
                        p.hit(card)
                        cards.append(int(card))
            all_cards.append(cards)
        self.state = States.DEALER
        return all_cards
        
    def play_dealer(self):
        if self.state != States.DEALER:
            return []
        cards = []
        while self.dealer.playing():
            match self.dealer.decision():
                case "S":
                    pass
                case "H":
                    card, *self.deck = self.deck
                    self.dealer.hit(card)
                    cards.append(int(card))
        self.state = States.RESULTS
        return cards

    def results(self):
        if self.state != States.RESULTS:
            return ""
        dealer_status = self.dealer.status()
        dealer_total = self.dealer.total
        messages = []
        for p in self.players:
            match p.status():
                case 1:
                    if dealer_status == 1:
                        messages.append([f"Both the dealer and player {p} got a natural blackjack, they push.", 0])
                    else:
                        messages.append([f"Player {p} got a natural blackjack and wins the bonus payout.", 1.5])
                case 2:
                    if dealer_status == 1:
                        messages.append([f"The dealer had natural blackjack, {p} loses.", -1])
                    elif dealer_status == 2:
                        messages.append([f"Both the dealer and player {p} got a blackjack, they push.", 0])
                    else:
                        messages.append([f"Player {p} got blackjack after hitting and wins", 1])
                case 3:
                    match dealer_status:
                        case 1:
                            messages.append([f"The dealer had natural blackjack, player {p} loses.", -1])
                        case 2:
                            messages.append([f"The dealer got a blackjack, player {p} loses.", -1])
                        case 3:
                            s = f"Player {p} stood on {p.total} and the dealer stood on {dealer_total},"
                            result = 0
                            if p.total > dealer_total:
                                s+= f" {p} wins."
                                result = 1
                            elif p.total < dealer_total:
                                s += f" {p} loses."
                                result = -1
                            else:
                                s += f" they push."
                            messages.append([s, result])
                        case 4:
                            messages.append([f"Player {p} stood on {p.total} and the dealer busted, {p} wins.", 1])
                case 4:
                    messages.append([f"Player {p} busted and lost.", -1])
        self.state = States.READY
        return messages


        
# dq = agent.DeepQAgent()
# p = agent.ProbAgent()