import curses
from time import sleep
from levelmanager import LevelManager
import platform
import threading


class Sokoban():
    """
        Sokoban class main game
        TODO: Fix timer window
        TODO: Make timer count based on time.time()
    """
    OBS = "██"
    EMP = "  "
    if ("windows" in platform.system().lower() or
            "microsoft" in platform.uname()[3].lower()):
        HER = "\u263A "
        BOX = "\u25CB "
        DES = "\u25D9 "
    else:
        BOX = "💩 "
        HER = "😐 "
        DES = "🚽 "

    def timer_update(self):
        self._timer += 1
        self._timerWin.clear()
        self._timerWin.box()
        message = f"{self._timer//60 % 60}:{self._timer % 60}"
        self.add_str_centered_x(self._timerWin, 1, message)
        self._timerWin.refresh()

    def show_timer(self):
        while self.timer_active:
            self.timer_update()
            sleep(1)

    def stop_timer(self):
        self.timer_active = False
        time_t = self._timer
        self._timer = 0
        return time_t

    @staticmethod
    def show_flashes(number):
        for itr in range(number):
            curses.flash()
            sleep(0.1)

    @staticmethod
    def add_str_centered_x(win, y, str):
        _, tar_x = win.getmaxyx()
        tar_x = (tar_x - len(str)) // 2
        win.addstr(y, tar_x, str)

    @staticmethod
    def add_subpad_centered_yx(win, lines, cols):
        tar_y, tar_x = win.getmaxyx()
        tar_y = (tar_y - lines) // 2
        tar_x = (tar_x - cols) // 2
        return win.subpad(lines, cols, tar_y, tar_x)

    @staticmethod
    def add_subpad_bottom_y(win, lines, cols):
        tar_y, tar_x = win.getmaxyx()
        tar_y = tar_y - lines - 1
        tar_x = (tar_x - cols) // 2
        return win.subpad(lines, cols, tar_y, tar_x)

    def show_box(self, message: list, min_lines=0, min_cols=0):
        self._mainWin.clear()
        lines = max(len(message) + 2, min_lines + 2)
        cols = max(max([len(line) for line in message]) + 4, min_cols + 2)
        sub_pad = self.add_subpad_centered_yx(self._mainWin, lines, cols)
        sub_pad.box()
        for line in range(len(message)):
            self.add_str_centered_x(sub_pad, line + 1, message[line])
        sub_pad.refresh()

    def show_controls(self):
        controls = ["WELCOME TO SOKOBAN",
                    " ",
                    "ARROWS - move",
                    "u - undo last move",
                    "r - reload level",
                    "n - skip level",
                    "q - quit",
                    "c - show controls",
                    " ",
                    "PRESS ANY KEY"]
        self.show_box(controls)
        self._mainWin.getkey()

    def win(self, score, moves):
        self.show_flashes(3)
        message = ["YOU WON", f"Moves made: {moves}", f"Score: {score}"]
        self.show_box(message)
        sleep(2)

    def skip(self):
        message = ["LEVEL SKIPPED ;(", "Score: 0"]
        self.show_box(message)
        sleep(2)

    def quit(self):
        message = [" ", "See you soon:)"]
        self.show_box(message, 3)
        sleep(2)

    def timer_loop(self):
        self._timer = 0
        self.timer_active = True
        timer_tread = threading.Thread(target=self.show_timer)
        timer_tread.daemon = True
        timer_tread.start()

    def loop(self):
        self.draw_level()
        self.timer_loop()
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
                self._timer = 0
                self._level.restart()
            elif event == 'c':
                self.show_controls()
            elif event == 'n':
                self.stop_timer()
                return 0, 0, 0
            elif event == 'q':
                self.stop_timer()
                return -1, 0, 0
            self.draw_level()
            if self._level.is_win():
                self.stop_timer()
                return 1, self._level.score, self._level.moves

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
        curses.curs_set(0)
        self._mainWin.keypad(True)

        self._levelManager = LevelManager()
        self._levelManager.load_levels()

        self.add_str_centered_x(self._mainWin, 5, f"Loaded from file {len(self._levelManager)} levels.")
        sleep(0.5)
        self.show_controls()

        for level in self._levelManager:
            self._mainWin.clear()
            self._mainWin.refresh()

            self._level = level

            self._gameWin = self.add_subpad_centered_yx(self._mainWin,level.height+6, level.width*2+6)
            self._gameWin.border()

            self._timerWin = self.add_subpad_bottom_y(self._mainWin, 3, 20)
            self._timerWin.border()

            try:
                result, score, moves = self.loop()
            except Exception as e:
                self._mainWin.addstr(1, 0, f"EXCEPTION OCCURED: {e}")
                self._mainWin.refresh()
                sleep(2)
                break
            else:
                if not result:
                    self.skip()
                elif result == 1:
                    self.win(score, moves)
                elif result == -1:
                    self.quit()
                    break

        curses.noraw()
        curses.echo()
        curses.endwin()



if __name__ == "__main__":
    game = Sokoban()
    game.run()
