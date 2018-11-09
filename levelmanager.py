from level import Level

class LevelManager():
    """
        LevelManager class(saves, loads from disk, give exact level etc.)
    """
    def __init__(self, path = None):
        self._path = path if path else "levels/classic.json"
        self._levels = None

    def __iter__(self):
        for level in levels:
            yield level

    def load_levels(self):
        pass

    def __getitem__(self, item):
        return self._levels[item]
