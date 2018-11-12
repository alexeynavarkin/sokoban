import curses
from time import sleep
from levelmanager import LevelManager
import platform


class Sokoban():
    """
        Sokoban class main game
        TODO: make method to show centered window with custom message
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

    def add_str_centered_x(self, win, y, str):
        _, tar_x = win.getmaxyx()
        tar_x = (tar_x - len(str)) // 2
        win.addstr(y, tar_x, str)

    def add_subpad_centered_yx(self, win, lines, cols):
        tar_y, tar_x = win.getmaxyx()
        tar_y = (tar_y - lines) // 2
        tar_x = (tar_x - cols) // 2
        return win.subpad(lines, cols, tar_y, tar_x)

    def win(self, score):
        self._mainWin.clear()
        sub_pad = self.add_subpad_centered_yx(self._mainWin, 5, 20)
        sub_pad.box()
        curses.flash()
        sleep(0.1)
        curses.flash()
        sleep(0.1)
        curses.flash()
        sleep(0.1)
        curses.flash()
        self.add_str_centered_x(sub_pad, 1, "YOU WON")
        self.add_str_centered_x(sub_pad, 2, f"Score: {score}")
        sub_pad.refresh()
        sleep(2)

    def skip(self):
        self._mainWin.clear()
        sub_pad = self.add_subpad_centered_yx(self._mainWin, 5, 20)
        sub_pad.box()
        self.add_str_centered_x(sub_pad, 1, "LEVEL SKIPPED ;(")
        self.add_str_centered_x(sub_pad, 2, "Score: 0")
        sub_pad.refresh()
        sleep(2)

    def quit(self):
        self._mainWin.clear()
        sub_pad = self.add_subpad_centered_yx(self._mainWin, 5, 20)
        sub_pad.box()
        self.add_str_centered_x(sub_pad, 2, "See you soon:)")
        # sub_pad.addstr(2, 4, "Scored: 0") # maybe add skored by session?
        sub_pad.refresh()
        sleep(2)


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

            self._gameWin = self.add_subpad_centered_yx(self._mainWin,level.height+6, level.width*2+6)
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
                    self.skip()
                elif result == 1:
                    self.win(score)
                elif result == -1:
                    self.quit()
                    break

        curses.noraw()
        curses.echo()
        curses.endwin()



if __name__ == "__main__":
    # wrapper need for fix terminal after failure
    game = Sokoban()
    game.run()
