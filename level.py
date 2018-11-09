from collections.abc import Sequence

class Level(Sequence):
    """
        Level class(moves, history, state)
    """
    def __init__(self):
        self._height = 11
        self._width = 19
        self._player_pos = (11, 8)
        self._data = [[0,0,0,0,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,3,0,0,0,3,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,3,2,0,0,3,0,0,0,0,0,0,0,0,0,0],
                     [0,0,3,3,3,0,0,2,3,3,0,0,0,0,0,0,0,0,0],
                     [0,0,3,0,0,2,0,2,0,3,0,0,0,0,0,0,0,0,0],
                     [3,3,3,0,3,0,3,3,0,3,0,0,0,3,3,3,3,3,3],
                     [3,0,0,0,3,0,3,3,0,3,3,3,3,3,0,0,4,4,3],
                     [3,0,2,0,0,2,0,0,0,0,0,0,0,0,0,0,4,4,3],
                     [3,3,3,3,3,0,3,3,3,0,3,1,3,3,0,0,4,4,3],
                     [0,0,0,0,3,0,0,0,0,0,3,3,3,3,3,3,3,3,3],
                     [0,0,0,0,3,3,3,3,3,3,3,0,0,0,0,0,0,0,0]]
        self._history = []

    def __getitem__(self, item):
        return self._data[item]

    def __len__(self):
        return len(self._data)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def move_up(self):
        pass

    def move_down(self):
        pass

    def move_right(self):
        pass

    def move_left(self):
        pass

    def undo(self):
        pass

    def is_win(self):
        pass

    def restart(self):
        pass