
class Thing:
    description = "A Generic thing"
    category = "Thing"
    letter = "*"

    # What am I made of?
    material = ["Stuff"]

    pickupable=True
    creature = False
    movable = True
    passable = True
    opaque = True
    damagable = False
    leaves_corpse = False
    decomposing = False
    decomposable = False

    dimensionality = 1
    weight=1
    speed=1

    # Hit points are only meaningful if damagable
    hp=0
    hitdice=0
    experience_value=0

    # Location of self in level
    idx = 0

    action_set ={}

    def removefrom(self,item_list):
        # Recursively search for self and remove self from an item list
        for x in item_list:
            if x is self:
                item_list.remove(x)
            else:
                # check if item is a container, and if so check in there
                self.remove_from(x.item_list)

    def destruct(self,world):
        # Remove self from the world
        # (we check all levels incase we have turned up somewhere odd)a
        for l in world.levels:
            self.removefrom(l.item_lists)
                
        # ... and from the player's inventory in case it is there.
        self.removefrom(world.player.inventory)
        
        return

    def acted_upon(self,context,who,what_happened,with_what,where,why):
        # Something happened to me, so do something about it
        if what_happened in self.action_set:
            action=self.action_set[what_happened]
            action(self,context,who,what_happened,with_what,where,why)
        return

    def describe_self(self):
        # XXX Does not show discovered information
        return self.description

    def accept_damage(self,context,who,what_happened,with_what,where,why,hp):
        self.hp = self.hp - hp
        if self.hp<=0:
            # Note how many hp were not consumed, as the caller might
            # want to know
            hp=-self.hp
            # Now die
            self.acted_upon(self,context,None,"die",None,where,why)
        else:
            hp=0
        return hp

    def die(self,context,who,what_happened,with_what,where,why,hp):
        # Counts for destruction as well.
        if self.creature:
            context.message.append("You killed "+self.description)
        else:
            context.message.append("You destroyed "+self.description)
        context.award_experience(self.experience_value)
        if self.leaves_corpse:
            self.description="A "+self.description+" corpse."
            self.action_list["tick"]=self.decompose
        else:
            self.destruct(context)
        return 0

    def decompose(self,context,who,what_happened,with_what,where,why,hp):
        return 0

class Item(Thing):
    def __init__(self):
        self.description = "A generic item"
        self.category = "Item"
        return

class Creature(Thing):
    creature = True
    damagable = True

class Monster(Item):
    def __init__(self):
        Item.__init__(self)
        self.description="Generic Monster"
        self.category="Monster"
        self.letter="m"
        self.hp=6
        self.hitdice=1
        self.speed=0.5
        self.experience_value=1
        self.action_set["hit"]=Monster.accept_damage
        self.action_set["die"]=Monster.die
        self.action_set["tick"]=Monster.monster_ai

        self.pickupable=False
        self.weight=160

    def monster_ai(self,context,who,what_happened,with_what,where,why):
        # Seek out the player, unless they are too scary

        # Find paths to player
        # XXX Cull out paths that are not discernable, e.g., blocked
        # by big things that prevent line of sight to the player,
        # unless monster can see through the blocking material type.

        # Take into account speed of monster, both slower than normal
        # and faster than normal.
        # Slow monster movement is implemented using randomisation
        # rather than tick counting.
        if self.speed<1:
            if random.random()<self.speed:
                speed=1
            else:
                speed=0
        else:
            speed=self.speed
        for s in range(0,speed):
            d = context.paths_to_player(self.idx,self.dimensionality)
            # Pick one at random and move there
            if d!=None:
                self.idx = random.choice(d)
        return




class Stairs(Item):
    def __init__(self):
        Item.__init__(self)
        self.description="Some stairs leading down"
        self.category="Stairs"
        self.hp=0
        self.hitdice=0
        self.experience_value=0
        self.action_set["climb"]=Stairs.switch_level
        self.speed=0.2
        self.character=">"
        self.destination=None
        self.movable=False
        self.pickupable=False
        self.weight=1000

    def switch_level(self,context,who,what_happened,with_what,where,why):
        # Check letter and special destination to see where we should go
        if self.destination=="":
            # Exit the game
            # XXX Ask for confirmation
            context.message.append("Bye!")
            context.abort=True
            return
        if self.destination in context.levels:
            context.current_level=self.destination
            context.cur_level=context.levels[self.destination]
        else:
            raise Exception, "Stairs lead to nonexistent place"

        # XXX Place player on appropriate stairs
        context.player.idx=0
                            
        return 0
