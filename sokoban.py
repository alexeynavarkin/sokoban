import curses
from time import sleep, time
from levelmanager import LevelManager
from BaseGame import BaseGame
import platform
import threading


NAME = "Sokoban"


class Game(BaseGame):
    def run(self):
        game = Sokoban()
        game.run()
        self.add_scores(game.score)


class Sokoban:
    """
        Sokoban class main game
    """
    def __init__(self):
        self.OBS = "██"
        self.EMP = "  "
        if ("microsoft" in platform.uname()[3].lower() or
                "windows" in platform.system().lower()):
            self.HER = "\u263A "
            self.BOX = "\u25CB "
            self.DES = "\u25D9 "
        else:
            self.BOX = "💩 "
            self.HER = "😐 "
            self.DES = "🚽 "
        self._score = self._timer = self.time_paused = 0
        self._time_start = None
        self._timer_hold = self._game_hold = self._timer_active = False
        self._timer_running = False
        self._levelManager = LevelManager()
        self._mainWin = self._gameWin = self._timerWin = self._level = None

    def time_str(self):
        minutes = str(self._timer // 60 % 60)
        if len(minutes) < 2:
            minutes = "".join(("0", minutes))
        seconds = str(self._timer % 60)
        if len(seconds) < 2:
            seconds = "".join(("0", seconds))
        return f"{minutes}:{seconds}"

    def timer_update(self):
        while self._timer_hold:
            self.wait()
        if self._timer_running:
            self._game_hold = True
            self._timer = int(time() - self._time_start)
            self._timerWin.clear()
            self._timerWin.box()
            self.add_str_centered_x(self._timerWin, 1, self.time_str())
            self._timerWin.refresh()
            self._game_hold = False

    def pause_timer(self):
        self._timer_running = False
        self.time_paused = time()

    def resume_timer(self):
        time_delta = time() - self.time_paused
        self._time_start += time_delta
        self._timer_running = True

    def show_timer(self):
        while self._timer_active:
            self.timer_update()
            sleep(0.5)

    def stop_timer(self):
        self._timer_active = self._timer_running = False
        time_t = self._timer
        self._timer = 0
        self._time_start = None
        return time_t

    def clear_timer(self):
        self._timer = self.time_paused = 0
        self._timer_hold = False
        self._game_hold = False
        self._time_start = time()

    def start_timer_loop(self):
        self.clear_timer()
        self._timer_active = self._timer_running = True
        timer_tread = threading.Thread(target=self.show_timer)
        timer_tread.daemon = True
        timer_tread.start()

    def clear_win(self, win):
        while self._game_hold:
            self.wait()
        self._timer_hold = True
        win.clear()
        self._timer_hold = False

    def refresh_win(self, win):
        while self._game_hold:
            self.wait()
        self._timer_hold = True
        win.refresh()
        self._timer_hold = False

    @staticmethod
    def wait():
        sleep(0.05)

    @staticmethod
    def show_flashes(number):
        for itr in range(number):
            curses.flash()
            sleep(0.1)

    @staticmethod
    def add_str_centered_x(win, y, string):
        _, tar_x = win.getmaxyx()
        tar_x = (tar_x - len(string)) // 2
        win.addstr(y, tar_x, string)

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

    def show_box(self, message: list, min_lines=0, min_cols=0, win=None):
        if win is None:
            win = self._mainWin
        self.clear_win(win)
        lines = max(len(message) + 2, min_lines + 2)
        cols = max(max([len(line) for line in message]) + 4, min_cols + 2)
        sub_pad = self.add_subpad_centered_yx(win, lines, cols)
        sub_pad.box()
        for line in range(len(message)):
            self.add_str_centered_x(sub_pad, line + 1, message[line])
        self.refresh_win(sub_pad)
        return sub_pad

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
        control_box = self.show_box(controls)
        self._mainWin.getkey()
        self.clear_win(control_box)
        self.refresh_win(control_box)

    def win(self, score, moves):
        self.show_flashes(3)
        message = ["YOU WON", f"Moves made: {moves}", f"Score: {score}"]
        self.show_box(message)
        sleep(2)

    def skip(self):
        message = ["LEVEL SKIPPED ;(", "Score: 0"]
        msg_box = self.show_box(message)
        sleep(2)
        self.clear_win(msg_box)
        self.refresh_win(msg_box)

    def quit(self):
        message = [" ", "See you soon:)"]
        msg_box = self.show_box(message, 3)
        sleep(2)
        self.clear_win(msg_box)
        self.refresh_win(msg_box)

    @property
    def score(self):
        return self._score

    def loop(self):
        self.start_timer_loop()
        self.draw_level()
        while True:
            event = self._mainWin.getkey()
            result = False
            if event == 'KEY_UP':
                result = self._level.move_up()
            elif event == 'KEY_DOWN':
                result = self._level.move_down()
            elif event == 'KEY_LEFT':
                result = self._level.move_left()
            elif event == 'KEY_RIGHT':
                result = self._level.move_right()
            elif event == 'u':
                result = self._level.undo()
            elif event == 'r':
                self.clear_timer()
                result = self._level.restart()
            elif event == 'c':
                self.pause_timer()
                self.show_controls()
                self.resume_timer()
                self.draw_level()
            elif event == 'n':
                self.stop_timer()
                return 0, 0, 0
            elif event == 'q':
                self.stop_timer()
                return -1, 0, 0
            if result:
                self.draw_level()
            if self._level.is_win():
                total_time = self.stop_timer()
                self._level.time_score(total_time)
                return 1, self._level.score, self._level.moves

    def draw_level(self):
        # self.clear_win(self._gameWin)
        # self._mainWin.clear()
        while self._game_hold:
            self.wait()
        self._timer_hold = True
        self.add_str_centered_x(self._mainWin, 2, self._level.name)
        c_y = 3
        for line in self._level:
            c_x = 3
            for symbol in line:
                c_sumbol = "  "

                if symbol == 0:
                    c_sumbol = self.EMP
                elif symbol == 1:
                    c_sumbol = self.HER
                elif symbol == 2:
                    c_sumbol = self.BOX
                elif symbol == 3:
                    c_sumbol = self.OBS
                elif symbol == 4:
                    c_sumbol = self.DES

                self._gameWin.addstr(c_y, c_x, c_sumbol)
                self.refresh_win(self._gameWin)
                c_x += 2
            c_y += 1
        self._timer_hold = False

    def new_screen(self):
        self._mainWin = curses.initscr()
        curses.noecho()
        curses.raw()
        curses.curs_set(0)
        self._mainWin.keypad(True)

    @staticmethod
    def remove_screen():
        curses.noraw()
        curses.echo()
        curses.endwin()

    def run(self):
        self.new_screen()
        self._levelManager.load_levels()

        self.add_str_centered_x(self._mainWin, 5,
                                "Loaded from file " +
                                f"{len(self._levelManager)} levels.")
        sleep(0.5)
        self.show_controls()

        for level in self._levelManager:
            self.clear_win(self._mainWin)
            self.refresh_win(self._mainWin)
            self._level = level

            self._gameWin = self.add_subpad_centered_yx(self._mainWin,
                                                        level.height + 6,
                                                        level.width * 2 + 6)
            self._gameWin.border()

            self._timerWin = self.add_subpad_bottom_y(self._mainWin, 3, 20)
            self._timerWin.border()

            try:
                result, score, moves = self.loop()
            except Exception as e:
                self._mainWin.addstr(1, 0, f"EXCEPTION OCCURED: {e}")
                self.refresh_win(self._mainWin)
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
        self.remove_screen()


def main():
    game = Sokoban()
    game.run()


if __name__ == "__main__":
    # wrapper need for fix terminal after failure
    main()
