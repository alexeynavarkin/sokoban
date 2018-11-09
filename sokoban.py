import curses
from .level import Level
from .levelmanager import LevelManager


class Sokoban:
    """
        Sokoban class main game
    """
    def __init__(self):
        pass

    def loop(self):
        pass

    def run(self):
        curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.keypad(True)
        mainWin = curses.newwin()



        curses.noecho()
        curses.cbreak()
        curses.keypad(True)
        curses.endwin()



if __name__ == "__main__":
    # wrapper need for fix terminal after failure
    curses.wrapper(Sokoban.run())