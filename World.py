import Objects
import Ui
import Player
import Levels

class World:
    abort = False

    levels=Levels.AllLevels()
    current_level="1"
    cur_level=levels["1"]
    message=[]

    ui = None
    player = None
    
    def __init__(self,ui,player):
        # Record player and ui
        self.ui=ui
        self.player=player

        return

    def tick(self):
        # Allow items to take actions
        for idx in range(self.cur_level.width):
            for i in self.cur_level.item_lists[idx]:
                i.acted_upon(self,None,"tick",None,idx,"tick")

    def move_left(self):
        if 0 == self.player.idx:
            self.player.happy = False
        else:
            self.player.idx = self.player.idx - 1
        self.tick()
        
    def move_right(self):
        if self.cur_level.width-1 == self.player.idx:
            self.player.happy = False
        else:
            self.player.idx = self.player.idx + 1
        self.tick()

    def climb_up(self):
        for i in self.cur_level.item_lists[self.player.idx]:
            if isinstance(i,Objects.Stairs):
                if i.letter=="<":
                    # Bingo, lets go up
                    i.acted_upon(self,None,"climb",None,i.idx,"climb")
                    return
        self.message.append("There are no stairs up here.")
    def climb_down(self):
        for i in self.cur_level.item_lists[self.player.idx]:
            if isinstance(i,Objects.Stairs):
                if i.letter==">":
                    # Bingo, lets go down
                    i.acted_upon(self,None,"climb",None,self.player.idx,"climb")
                    return
        self.message.append("There are no stairs down here.")

    def pickup_item(self):
        raise Exception, 'not yet implemented'
    def drop_item(self):
        raise Exception, 'not yet implemented'

    def paths_to_player(self,idx,dimensionality):
        # XXX Doesn't offer higher-dimensional paths yet
        paths=[]
        if idx < self.player.idx:
            paths.append(idx+1)
        elif idx > self.player.idx:
            paths.append(idx-1)
        else:
            # Already there
            paths.append(idx)
        return paths

    def look_here(self):
        count=0
        item_list=self.cur_level.item_lists[self.player.idx]
        for i in item_list:
            # Item is here, so display it.
            if count==0:
                self.message.append("You see here: ")
            count=count+1
            self.message.append(i.describe_self())
        if count==0:
            self.message.append("There is nothing here.")

    def abort(self):
        self.abort=True

    def render(self):
        # Draw the world
        return str(self.cur_level.render(self))+"\nLevel "+self.cur_level.description+"\n"

    def process_char(self,c):
        switch = { 'l': self.move_right
                 , 'h': self.move_left
                 , '<': self.climb_up
                 , '>': self.climb_down
                 , ',': self.pickup_item
                 , 'd': self.drop_item
                 , ':': self.look_here
                 , 'q': self.abort
                 }
        if c in switch:
            switch[c]()
            return 0
        else:
            return -1

    def doturn(self):
        # Get input from user
        c = self.ui.getch()
        # Process input from user (possibly causing the world to tick)
        self.process_char(c)
        # Give the user an updated view of the world
        self.ui.redraw()
        return
