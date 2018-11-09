from collections.abc import Sequence
from level import Level

class LevelManager(Sequence):
    """
        LevelManager class(saves, loads from disk, give exact level etc.)
    """
    def __init__(self, path = None):
        self._path = path if path else "levels/classic.json"
        self._levels = []

    def __getitem__(self, item):
        return self._levels[item]

    def __len__(self):
        return len(self._levels)

    def load_levels(self):
        pass
