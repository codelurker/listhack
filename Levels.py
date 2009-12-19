import random
import Objects
    
def AllLevels():
        # Create level tree 
        level_list={}

        # Main trunk
        pl=""
        for l in range(1,21):
           tl=str(l)
           nl=str(l+1)
           level_list[tl]=Level(tl,"Normal",[pl],[nl])
           pl=tl

        return level_list


class Level:
    description=None
    level_type="Normal"

    width=1
    k=1
    n=1

    item_lists=[]

    def __init__(self,desc,level_type,ups,downs):
       if level_type == None:
          level_type="Normal"
      
       self.level_type=level_type
       self.description=desc
       self.choose_topology(None)
       self.install_stairs("<",ups)
       self.install_stairs(">",downs)
       self.populate_level()
    
    def render(self,world):
        # Draw level background using k and n to dictate level dimensions
        b="."*self.width
        d=[]
        d.extend(b)

        # Render the items on the level
        for idx in range(1,self.width):
           for i in self.item_lists[idx]:
              d[idx]=i.letter

        d[world.player.idx]='@'
        s=""
        for c in d:
           s=s+c

        return s


    def choose_topology(self,max_dimensionality):
      if max_dimensionality == None:
         max_dimensionality=6
      if max_dimensionality>6:
         max_dimensionality=6
      if max_dimensionality<1:
         max_dimensionality=1
      
      # Generate possible topologies
      topologies=[]
      if max_dimensionality == 1:
         # 1D level, so free size selection
         n=random.randint(16,78)
      else:
          # 2-6D, so make it an n**k, k>=2
         for n in range(1,8):
            for k in range(1,max_dimensionality):
               if n**k<79:
                  topologies.append([n,k])
        
      # Having got the possible topologies, pick one
      topology=random.choice(topologies)
      self.n=topology[0]
      self.k=topology[1]
      self.width=self.n**self.k

      self.item_lists=[]
      for idx in range(0,self.width):
         self.item_lists.append([])
      
    def populate_level(self):
        return
      
    def install_stairs(self,letter,destinations):
        for d in destinations:
           s=Objects.Stairs()
           s.letter=letter
           s.destination=d
           s.description="Some stairs"
           # Stairs can be on top of each other, this is okay.
           idx=random.randint(0,self.width-1);
           l=self.item_lists[idx]
           l.append(s)

    def tick(self,world):
      for idx in range(1,self.width):
         l=self.item_lists[idx]
         for i in l:
            i.acted_upon(self,None,"tick",None,idx,"tick")
