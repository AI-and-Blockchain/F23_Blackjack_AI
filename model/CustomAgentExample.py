from random import randint

class Agent: # Abstract Agent class
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"
    def __str__(self):
        return f"{self.id}"
    def add_card(self, card: int, total: int):
        raise Exception("Not yet implemented")
    def add_dealer_card(self, card: int):
        raise Exception("Not yet implemented")
    def decision(self) -> str:
        raise Exception("Not yet implemented")
    def start_new(self):
        raise Exception("Not yet implemented")

class CustomAgent(Agent): # your implmentation goes here
     # Accept only an id as an input, and ensure that self.id gets set as such
    def __init__(self, id):
        self.id = id

    # accept a card from the hand, as well as a precalculated total
    def add_card(self, card: int, total: int):
        pass

    # accept the dealer's card that is face-up
    def add_dealer_card(self, card: int):
        pass
    
    # make a decision based on the data available, always return "S" or "H"
    def decision(self) -> str:
        return 'S' if randint(0,1) == 1 else 'H'
    
    # prepare the agent for a new round, this can be changed but must be callable
    def start_new(self):
        self.cards = []
        self.total = 0