import curses
from time import sleep
from level import Level
from levelmanager import LevelManager
import platform


class Sokoban():
    """
        Sokoban class main game
    """
    OBS = "██"
    EMP = "  "
    if "microsoft" in platform.uname()[3].lower():
        HER = "\u263A "
        BOX = "\u25CB "
        DES = "\u25D9 "
    else:
        BOX = "💩 "
        HER = "😐 "
        DES = "🚽 "

    def loop(self):
        self.draw_level()
        while True:
            event = self._mainWin.getkey()

            if   event == 'KEY_UP':
                self._level.move_up()
            elif event == 'KEY_DOWN':
                self._level.move_down()
            elif event == 'KEY_LEFT':
                self._level.move_left()
            elif event == 'KEY_RIGHT':
                self._level.move_right()
            elif event == 'u':
                self._level.undo()
            elif event == 'r':
                self._level.restart()
            elif event == 'n':
                return 0, 0
            elif event == 'q':
                return -1, 0

            self.draw_level()

            if self._level.is_win():
                return 1, self._level.score

    def draw_level(self):
        c_y = 3
        for line in self._level:
            c_x = 3
            for symbol in line:
                c_sumbol = "  "

                if symbol == 0:
                    c_sumbol = Sokoban.EMP
                elif symbol == 1:
                    c_sumbol = Sokoban.HER
                elif symbol == 2:
                    c_sumbol = Sokoban.BOX
                elif symbol == 3:
                    c_sumbol = Sokoban.OBS
                elif symbol == 4:
                    c_sumbol = Sokoban.DES

                self._mainWin.refresh()
                self._mainWin.addstr(0, 0, f"   DRAW {symbol} AT ({c_y},{c_x})   ")
                self._gameWin.addstr(c_y, c_x, c_sumbol)
                self._gameWin.refresh()
                c_x += 2
            c_y += 1
            self._gameWin.refresh()

    def run(self):
        self._mainWin = curses.initscr()
        curses.noecho()
        curses.raw()
        # curses.cbreak() # WTF
        self._mainWin.keypad(True)
        max_y, max_x = self._mainWin.getmaxyx()

        self._levelManager = LevelManager()
        self._levelManager.load_levels()

        self._mainWin.addstr(1, 0, f"Loaded from disk {len(self._levelManager)} levels.")
        self._mainWin.refresh()
        sleep(2)

        for level in self._levelManager:
            self._mainWin.clear()
            self._mainWin.refresh()

            self._level = level

            gameWinY = max_y // 2 - level.height
            gameWinX = max_x // 2 - level.width

            self._mainWin.addstr(1, 0, level.name)
            self._mainWin.addstr(max_y-2, 0, f"GAME_WIN:({gameWinY},{gameWinX}) ({level.height},{level.width})")

            self._gameWin = self._mainWin.subwin(level.height+6, level.width*2+6, gameWinY, gameWinX)
            self._gameWin.border()
            self._gameWin.refresh()
            sleep(1)

            try:
                result, score = self.loop()
            except Exception as e:
                self._mainWin.addstr(1, 0, f"EXCEPTION OCCURED: {e}")
                self._mainWin.refresh()
                sleep(2)
                break
            else:
                if result == 1:
                    self._mainWin.addstr(1, 0, "GOT WIN")
                    sleep(2)
                elif result == -1:
                    self._mainWin.addstr(1, 0, "GOT QUIT CMD")
                    self._mainWin.refresh()
                    sleep(2)
                    break


        self._mainWin.keypad(False)
        # curses.nocbreak() # WTF
        curses.noraw()
        curses.echo()
        curses.endwin()



if __name__ == "__main__":
    # wrapper need for fix terminal after failure
    game = Sokoban()
    game.run()