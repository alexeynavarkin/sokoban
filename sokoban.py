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

    def win(self, result, score):
        self._mainWin.clear()
        self._gameWin.untouchwin()
        max_y, max_x = self._mainWin.getmaxyx()
        sub_pad = self._mainWin.subpad(5,20,max_y//2-1,max_x//2-10)
        sub_pad.box()
        curses.flash()
        sleep(0.1)
        curses.flash()
        sleep(0.1)
        curses.flash()
        sleep(0.1)
        curses.flash()
        sub_pad.addstr(1, 1, f"YOU WON! {result} {score}")
        sub_pad.refresh()
        sleep(2)

    def skip(self):
        self._mainWin.clear()
        self._gameWin.untouchwin()
        max_y, max_x = self._mainWin.getmaxyx()
        sub_pad = self._mainWin.subpad(5, 20, max_y // 2 - 1, max_x // 2 - 10)
        sub_pad.box()
        sub_pad.addstr(1, 1, "LEVEL SKIPPED")
        sub_pad.refresh()


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

                self._gameWin.addstr(c_y, c_x, c_sumbol)
                self._gameWin.refresh()
                c_x += 2
            c_y += 1

    def run(self):
        self._mainWin = curses.initscr()
        curses.noecho()
        curses.raw()
        self._mainWin.keypad(True)

        max_y, max_x = self._mainWin.getmaxyx()

        self._levelManager = LevelManager()
        self._levelManager.load_levels()

        self._mainWin.addstr(max_y//2, max_x//2, f"Loaded from disk {len(self._levelManager)} levels.")
        self._mainWin.refresh()
        sleep(0.5)

        for level in self._levelManager:
            self._mainWin.clear()
            self._mainWin.refresh()

            self._level = level

            gameWinY = max_y // 2 - level.height
            gameWinX = max_x // 2 - level.width

            self._gameWin = self._mainWin.subpad(level.height+6, level.width*2+6, gameWinY, gameWinX-3)
            self._gameWin.border()

            try:
                result, score = self.loop()
            except Exception as e:
                self._mainWin.addstr(1, 0, f"EXCEPTION OCCURED: {e}")
                self._mainWin.refresh()
                sleep(2)
                break
            else:
                if not result:
                    self._mainWin.addstr(1, 0, "LEVEL SKIPPED")
                    self._mainWin.refresh()
                    sleep(2)
                elif result == 1:
                    self.win(result, score)
                elif result == -1:
                    self._mainWin.addstr(1, 0, "GOT QUIT CMD")
                    self._mainWin.refresh()
                    sleep(2)
                    break

        curses.noraw()
        curses.echo()
        curses.endwin()



if __name__ == "__main__":
    # wrapper need for fix terminal after failure
    game = Sokoban()
    game.run()