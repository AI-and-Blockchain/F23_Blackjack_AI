class Agent: # Abstract Agent class
    def __init__(self):
        self.id = 0
    def __repr__(self):
        return f"{self.id}"

class DeepQAgent(Agent):
    def __init__(self):
        super().__init__()
        self.id = 1
    
class ProbAgent(Agent):
    def __init__(self):
        super().__init__()
        self.id = 2
        
class User:
    def __init__(self):
        self.id = 3
    def __repr__(self):
        return f"{self.id}"