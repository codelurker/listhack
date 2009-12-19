#!/bin/env python
#
# ListHack : a 1D text adventure game
#

import sys
#import twitter
import Ui
import World
import Objects
import Player

def main():

    #if len(sys.argv) >1:
       #print "Using console UI"
       #ui=Ui.ConsoleUi()
    #else: 
       #ui=Ui.DefaultUi()
    ui=Ui.ConsoleUi() # xxx

    player = Player.Player(ui)
    world = World.World(ui,player)

    ui.setplayer(player)
    ui.setworld(world)

    world.ui.redraw()
    while world.abort != True:
        world.doturn()
        
    ui.close()

if __name__ == '__main__':
    main()
