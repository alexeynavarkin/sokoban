import re
import json
from level import Level
from collections.abc import Sequence

class LevelManager(Sequence):
    """
        LevelManager class(saves, loads from disk, give exact level etc.)
    """
    def __init__(self, path = None):
        self._path = path if path else "classic.json"
        self._levels = []
        self.levels = []

    def __getitem__(self, item):
        return self.levels[item]

    def __len__(self):
        return len(self.levels)

    def load_levels(self):
        with open("classic.json", "r") as file:
            parsed = json.load(file)
            for level in parsed:
                line = level["data"]
                line = line.split("*")
                level["data"] = line[2]
                level.update({"width": int(line[1])})
                level.update({"height": int(line[0])})
                self._levels.append(level)

            for level in self._levels:
                pattern = '.' * int(level["width"])
                data_list = re.findall(pattern, level["data"])
                buflist = []
                for line in data_list:
                    buflist.append([int(x) for x in line])
                level["data"]=buflist

            for level in self._levels:
                ll = Level(level["name"], level["data"], level["height"], level["width"])
                self.levels.append(ll)

if __name__ == "__main__":
    ll = LevelManager()
    ll.load_levels()
    for level in ll:
        print(level.height, level.width)
        for line in level:
            print(line)