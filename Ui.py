#!/bin/env python
#
# listhack, one-dimentional roguelike
#
from cStringIO import StringIO
curses_mode=0

try:
    import curses
    curses_mode=1
except:
    curses_mode=0
    print "WARNING: Curses not available.  Using line mode instead."
    pass

import random
import sys
import time
import traceback


class Ui(object):
    world = None
    player = None

    LORUM_IPSUM="Blah blah blah"

    def setworld(self,world):
        self.world=world

    def setplayer(self,player):
        self.player=player

    def __init__(self):
        # By default do nothing on construction
        return

    def redraw(self):
        raise Exception, 'UI must be able to draw itself'

    def write(self,text):
        raise Exception, 'UI must be able to accept user status messages'

    def close(self):
        # by default do nothing on close of ui
        return

    def prompt(self,message):
        raise Exception, 'UI must be able to prompt user for input'

    def getline(self):
        # Read a line of input with echo on and allowing user correction
        # Should also clear the prompt when done
        raise Exception, 'UI must be able to read a line of input'

    def getch(self):
        # Should be non-echoed, and not line-mode
        raise Exception, 'UI must be able to read a character of input'

    #
    # Utility functions for derived classes
    #
    def pad(s, char_count):
        return '%s%s'%(s, ' '*(char_count-len(s)))

class ConsoleUi(Ui):

    char_queue=[]

    def redraw(self):
        # Draw the world and character information.
        print
        for m in self.world.message:
            print m
        self.world.message=[]
        print self.world.render()
        print self.player.render()
        return

    def write(self,text):
        print text
        return

    def prompt(self,message):
        print message
        return

    def getch(self):
        while not len(self.char_queue):
            self.char_queue=[]
            self.char_queue.extend(sys.stdin.readline())

        r=self.char_queue[0]
        self.char_queue=self.char_queue[1::]
        return r

    def getline(self):
        # Clear queued chars if reading a line of input
        self.char_queue=[]
        return sys.stdin.readline()

    def close(self):
        print "Bye!"
        return

# --------------------------------------------------------
# Curses ui
# --------------------------------------------------------
#
# xxx would be nice to have the inventory displayed in the
# standard view. Perhaps a list down the right-hand side of
# the bottom window, leaving the console on the left.
#
class CursesUi(Ui):
    def __init__(self):
        self.stdscr = curses.initscr()
        self._draw()
    def redraw(self):
        # will be useful for window resizing events
        # be aware of this: http://bugs.python.org/issue984870
        self._draw()
    def _draw(self):
        size = self.stdscr.getmaxyx()
        # User message window
        self.win_msg = self.stdscr.derwin(1, size[1], 0, 0)
        # Separator of dashes
        self.win_sp1 = self.stdscr.derwin(1, size[1], 1, 0)
        # Window that the gameworld dimension shows in
        self.win_dim = self.stdscr.derwin(3, size[1], 2, 0)
        # Another separator
        self.win_sp2 = self.stdscr.derwin(1, size[1], 5, 0)
        # Console
        self.win_con = self.stdscr.derwin(size[0]-6, size[1]-20, 6, 0)
        # Inventory
        self.win_inv = self.stdscr.derwin(size[0]-6, 20, 6, size[1]-20)

        self.win_msg.addstr("Listhack")
        self.win_sp1.addstr("."*(size[1]-1))
        if self.world != None and self.world.cur_level != None:
            self.win_dim.addstr(self.world.cur_level.render(self.world))
        self.win_sp2.addstr("."*(size[1]-1))
        self.win_inv.addstr('inventory')
        self.win_inv.addstr(1, 0, self.LORUM_IPSUM[:300])

        self.console_lines = []
    def close(self):
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()
    def write(self, raw):
        for line in str(raw).split('\n'):
            msg = str(line).rstrip()
            size = self.win_con.getmaxyx()
            log('%s %s'%(time.strftime('* %Y%m%d %H:%M.%S'), msg))
            while len(msg) >= size[1]:
                self.console_lines.append(
                    pad(msg[:(size[1]-2)], size[1])
                )
                msg = msg[(size[1]-2):]
            self.console_lines.append( pad(msg, size[1]) )
            while len(self.console_lines) >= size[0]:
                del self.console_lines[0]
            for idx, line in enumerate(self.console_lines):
                self.win_con.addstr(idx, 0, line)
        self.win_con.refresh()
    def update(self):
        pass # xxx
    def getch(self):
        return self.stdscr.getch()


def DefaultUi():
    if curses_mode:
        return CursesUi()
    else:
        return ConsoleUi()
