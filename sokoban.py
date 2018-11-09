import curses
from level import Level
from levelmanager import LevelManager


class Sokoban:
    """
        Sokoban class main game
    """
    def __init__(self):
        self.BOX = "💩 "
        self.HER = "😐 "
        self.OBS = "██"
        self.EMP = "  "
        self.DES = "🌐 "

    def loop(self):
        while(True):
            self.draw_level()
            event = self._mainWin.getkey()
            if event == 'q':
                break
            elif event == 'KEY_UP':
                self._level.move_up()
            elif event == 'KEY_DOWN':
                self._level.move_down()
            elif event == 'KEY_LEFT':
                self._level.move_left()
            elif event == 'KEY_RIGHT':
                self._level.move_right()


    def draw_level(self):
        c_y = 0
        c_x = 0
        for line in self._level:
            c_y += 1
            c_x = 0
            # self._gameWin.move(c_line, 0)
            for symbol in line:
                c_x += 2
                c_sumbol = "  "
                if symbol == 0:
                    c_sumbol = self.EMP
                elif symbol == 1:
                    c_sumbol = self.HER
                elif symbol == 2:
                    c_sumbol = self.BOX
                elif symbol == 3:
                    c_sumbol = self.OBS
                elif symbol == 3:
                    c_sumbol = self.DES
                self._gameWin.addstr(c_y, c_x, c_sumbol)



    def run(self):
        self._mainWin = curses.initscr()
        curses.noecho()
        curses.raw()
        # curses.cbreak() # WTF
        self._mainWin.keypad(True)
        gameWinY, gameWinX= self._mainWin.getmaxyx()

        # self._levelManager = LevelManager()
        # for level in self._levelManager:
        self._level = Level() ## change for loop later
        gameWinY = (gameWinY) // 2 - self._level.height
        gameWinX = (gameWinX) // 2 - self._level.width
        self._gameWin = self._mainWin.subwin(self._level.height+4, self._level.width*2+4, gameWinY, gameWinX)
        self._gameWin.border()

        try:
            result = self.loop()
        except Exception as e:
            print(e)

        self._mainWin.keypad(False)
        # curses.nocbreak() # WTF
        curses.noraw()
        curses.echo()
        curses.endwin()



if __name__ == "__main__":
    # wrapper need for fix terminal after failure
    game = Sokoban()
    game.run()