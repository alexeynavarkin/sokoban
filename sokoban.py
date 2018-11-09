import curses
from level import Level
from levelmanager import LevelManager


class Sokoban:
    """
        Sokoban class main game
    """
    def __init__(self):
        pass

    def loop(self):
        while(True):
            event = self._mainWin.getkey()
            self._mainWin.addstr(event)
            self._mainWin.addstr('\n')
            if event == 'q':
                break
            elif event == '^C':
                break
            elif event == 'KEY_UP':
                lev

    def run(self):
        self._mainWin = curses.initscr()
        curses.noecho()
        curses.raw()
        # curses.cbreak() # WTF
        self._mainWin.keypad(True)
        gameWinY, gameWinX= self._mainWin.getmaxyx()
        gameWinY = (gameWinY-25) // 2
        gameWinX = (gameWinX-50) // 2
        self._mainWin.addstr(str(gameWinX))
        self._mainWin.addstr(str(gameWinY))
        self._gameWin = self._mainWin.subwin(25,50, gameWinY, gameWinX)
        self._gameWin.border()
        self._gameWin.addstr(1, 1, '░░')
        self._gameWin.addstr(2, 2, '░░')

        try:
            self.loop()
        except Exception:
            pass

        self._mainWin.keypad(False)
        # curses.nocbreak() # WTF
        curses.noraw()
        curses.echo()
        curses.endwin()



if __name__ == "__main__":
    # wrapper need for fix terminal after failure
    game = Sokoban()
    game.run()