from collections.abc import Sequence
from copy import deepcopy


class Level(Sequence):
    """
        Level class(moves, history, state)
    """
    def __init__(self, name, data: list):
        self._height = len(data)
        self._width = len(data[0])
        self._name = name
        self._data = tuple(deepcopy(data))
        self._cur = deepcopy(data)
        self._player_pos = self._find_player_pos()
        self._history = []

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self):
        return len(self._data)

    @property
    def name(self):
        return self._name

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def _find_player_pos(self):
        for line in range(len(self._cur)):
            if 1 in self._cur[line]:
                return line, self._cur[line].index(1)

    def _save(self):
        self._history.append(deepcopy(self._cur))

    def _check_cell(self, line, pos, cell_val):
        if line < 0 or line >= self.height or \
                pos < 0 or pos >= self.width or cell_val == 3:
            return False

    def _rec_cell(self, line, pos):
        if self._data[line][pos] == 4:
            return 4
        return 0

    def _move(self, d_line, d_pos):
        line, pos = self._player_pos
        dest_line, dest_pos = line + d_line, pos + d_pos
        dest_cell = self._cur[dest_line][dest_pos]

        if not self._check_cell(dest_line, dest_pos, dest_cell):
            return False

        if dest_cell == 0 or dest_cell == 4:
            self._save()
            self._cur[dest_line][dest_pos] = 1
            self._cur[line][pos] = self._rec_cell(line, pos)
            self._player_pos = (dest_line, dest_pos)
            return True

        if dest_cell == 2:
            next_line, next_pos = dest_line + d_line, dest_pos + d_pos
            next_cell = self._cur[next_line][next_pos]
            if next_cell == 2 or\
                    not self._check_cell(next_line, next_pos, next_cell):
                return False
            self._save()
            self._cur[next_line][next_pos] = 2
            self._cur[dest_line][dest_pos] = 1
            self._cur[line][pos] = self._rec_cell(line, pos)
            self._player_pos = (dest_line, dest_pos)
            return True

    def move_up(self):
        return self._move(-1, 0)

    def move_down(self):
        return self._move(1, 0)

    def move_right(self):
        return self._move(0, 1)

    def move_left(self):
        return self._move(0, -1)

    def undo(self):
        if len(self._history) == 0:
            return False
        self._cur = deepcopy(self._history[-1])
        self._player_pos = self._find_player_pos()
        del self._history[-1]
        return True

    def is_win(self):
        for line in range(len(self._data)):
            while 4 in self._data[line]:
                target_ind = self._data[line].index(4)
                if self._cur[line][target_ind] != 2:
                    return False
        return True

    def restart(self):
        self._cur = deepcopy(self._data)
        self._player_pos = self._find_player_pos()
        self._history.clear()
        return True
