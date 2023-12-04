from typing import List, Type
import numpy as np

from model.player import Agent, Dealer, LocalPlayer
from model.utils import States

# Game class that runs the logic of a blackjack game
# Uses states to correctly proceed through the steps of a game
class BlackjackGame:
    # can accept players on initialization, as well as set how many decks to run through
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
    
    # reset the game
    def revert(self):
        self.__init__()

    # Accept a one-time list of players if they were not provided on initialization
    def add_players(self, players: List[Type[Agent]]):
        if self.state != States.PLAYERS:
            return
        self.players = [LocalPlayer(p) for p in players]
        self.state = States.BET

    # a relic of old structure, no longer needed besides as a way to block until bets have been placed
    def bet(self):
        if self.state != States.BET:
            return
        self.state = States.READY

    # start the game by resetting all players to prepare for the deal
    def start(self):
        if self.state != States.READY:
            return
        self.dealer.start_new()
        for p in self.players:
            p.start_new()
        self.state = States.DEAL
        
    # loop across all players and the dealer to deal them cards from the shuffled deck
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
        # return the dealer's cards in a list, and the players' cards and hand totals in a list of lists
        return [int(card) for card in self.dealer.cards], [[[int(card) for card in p.cards], p.total] for p in self.players]
    
    # Accepts decisions from the frontend user on what to play
    def play_user(self, decision):
        if self.state != States.PLAY:
            return 0, True
        p = self.players[0]
        if not p.playing():
            self.state = States.AI
            return 0, False
        if decision == "S":
            p.stand()
            card = 0
        else:
            card, *self.deck = self.deck
            p.hit(card)
        if p.playing():
            return int(card), True
        else:
            # advance to the AI turns if the player is finished
            self.state = States.AI
            return int(card), False
    
    # instruct all AI agents to play their hands by polling moves until they stand or bust
    def play_AI(self):
        if self.state != States.AI:
            return []
        all_cards = []
        for p in self.players[1:]:
            cards = []
            while p.playing():
                if p.decision() == "S":
                    pass
                else:
                    card, *self.deck = self.deck
                    p.hit(card)
                    cards.append(int(card))
            all_cards.append(cards)
        self.state = States.DEALER
        return all_cards
    
    # instruct the dealer to play until it hits above 17 or busts
    def play_dealer(self):
        if self.state != States.DEALER:
            return []
        cards = []
        while self.dealer.playing():
            if self.dealer.decision() == "S":
                pass
            else:
                card, *self.deck = self.deck
                self.dealer.hit(card)
                cards.append(int(card))
        self.state = States.RESULTS
        return cards

    # calculate the losses and wins of each player and return the results, as well as a bet modifier for payouts
    def results(self):
        if self.state != States.RESULTS:
            return ""
        dealer_status = self.dealer.status()
        dealer_total = self.dealer.total
        messages = []
        for i, p in enumerate(self.players):
            if p.status() == 1:
                if dealer_status == 1:
                    messages.append([f"Both the dealer and {'player ' * (i == 0)}{p} got a natural blackjack, they push.", 0])
                else:
                    messages.append([f"{'Player ' * (i == 0)}{p} got a natural blackjack and wins the bonus payout.", 1.5])
            elif p.status() == 2:
                if dealer_status == 1:
                    messages.append([f"The dealer had natural blackjack, {p} loses.", -1])
                elif dealer_status == 2:
                    messages.append([f"Both the dealer and {'player ' * (i == 0)}{p} got a blackjack, they push.", 0])
                else:
                    messages.append([f"{'Player ' * (i == 0)}{p} got blackjack after hitting and wins", 1])
            elif p.status() == 3:
                if dealer_status == 1:
                    messages.append([f"The dealer had natural blackjack, {'player ' * (i == 0)}{p} loses.", -1])
                elif dealer_status == 2:
                    messages.append([f"The dealer got a blackjack, {'player ' * (i == 0)}{p} loses.", -1])
                elif dealer_status == 3:
                    s = f"{'Player ' * (i == 0)}{p} stood on {p.total} and the dealer stood on {dealer_total},"
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
                elif dealer_status == 4:
                    messages.append([f"{'Player ' * (i == 0)}{p} stood on {p.total} and the dealer busted, {p} wins.", 1])
            elif 4:
                messages.append([f"{'Player ' * (i == 0)}{p} busted and lost.", -1])
        self.state = States.READY
        return messages