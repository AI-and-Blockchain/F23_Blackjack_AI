class Agent: # Abstract Agent class
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"
    def __str__(self):
        return f"{self.id}"
    def add_card(self, card):
        raise Exception("Not yet implemented")
    def add_dealer_card(self, card):
        raise Exception("Not yet implemented")
    def decision(self):
        """
        Returns "S" for stand and "H" for hit
        """
        raise Exception("Not yet implemented")
    def start_new(self):
        raise Exception("Not yet implemented")

class CustomAgent(Agent): # your implmentation goes here
    def __init__(self, id):
        self.id = id

    def add_card(self, card, total):
        pass

    def add_dealer_card(self, card):
        pass
    
    def decision(self):
        return 'S'
    
    def start_new(self):
        self.cards = []
        self.total = 0