from abc import ABC, abstractmethod

class Behavior(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def action(self):
        pass
        
    @abstractmethod
    def surpress(self):
        pass
    
    @abstractmethod
    def takeControl(self):
        pass
        