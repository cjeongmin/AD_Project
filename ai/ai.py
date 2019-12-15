import sys, os
sys.path.insert(1, os.path.dirname(os.path.abspath(__package__))+"/ai")

from location import Location
from searcher import Searcher

class AI:
    board = (
        '         \n'  #   0 -  9
        '         \n'  #  10 - 19
        ' rnbqkbnr\n'  #  20 - 29
        ' pppppppp\n'  #  30 - 39
        ' ........\n'  #  40 - 49
        ' ........\n'  #  50 - 59
        ' ........\n'  #  60 - 69
        ' ........\n'  #  70 - 79
        ' PPPPPPPP\n'  #  80 - 89
        ' RNBQKBNR\n'  #  90 - 99
        '         \n'  # 100 -109
        '         \n'  # 110 -119
    )

    def __init__(self):
        self.hist = [Location(AI.board, 0, (True, True), (True, True), 0, 0)]
        self.searcher = Searcher()
        for k, table in self.hist[0].pst.items():
            padrow = lambda row: (0,) + tuple(x+self.hist[0].piece[k] for x in row) + (0,)
            self.hist[0].pst[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
            self.hist[0].pst[k] = (0,)*20 + self.hist[0].pst[k] + (0,)*20

    def parse(self, c):
        return 91 + (ord(c[0])-ord('a')) - 10*(int(c[1])-1)

    def render(self, i):
        rank, fil = divmod(i-91, 10)
        return chr(fil + ord('a')) + str(-rank + 1)