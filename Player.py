import Objects
import Ui
import World

class Player(Objects.Creature):

    character_class = None
    
    def __init__(self,ui):
        # Create a new character using ui to comminicate with the
        # player to answer any character generation questions        
        return

    def render(self):
        return "Bob the Character-Class"
