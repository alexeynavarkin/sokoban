from . import level

class LevelManager():
    """
        LevelManager class(saves, loads from disk, give exact level etc.)
    """
    def __init__(self, path = None):
        self._path = path if path else "levels/classic.json"
        pass

    def __iter__(self):
        pass
