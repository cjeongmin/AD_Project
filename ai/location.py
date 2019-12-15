from collections import namedtuple
from itertools import count

class Location(namedtuple('Location', 'board score wc bc ep kp')):
    piece = { 'P': 100, 'N': 280, 'B': 320, 'R': 479, 'Q': 929, 'K': 60000 }
    pst = {
        'P': (   0,   0,   0,   0,   0,   0,   0,   0,
                78,  83,  86,  73, 102,  82,  85,  90,
                7,  29,  21,  44,  40,  31,  44,   7,
            -17,  16,  -2,  15,  14,   0,  15, -13,
            -26,   3,  10,   9,   6,   1,   0, -23,
            -22,   9,   5, -11, -10,  -2,   3, -19,
            -31,   8,  -7, -37, -36, -14,   3, -31,
                0,   0,   0,   0,   0,   0,   0,   0),
        'N': ( -66, -53, -75, -75, -10, -55, -58, -70,
                -3,  -6, 100, -36,   4,  62,  -4, -14,
                10,  67,   1,  74,  73,  27,  62,  -2,
                24,  24,  45,  37,  33,  41,  25,  17,
                -1,   5,  31,  21,  22,  35,   2,   0,
            -18,  10,  13,  22,  18,  15,  11, -14,
            -23, -15,   2,   0,   2,   0, -23, -20,
            -74, -23, -26, -24, -19, -35, -22, -69),
        'B': ( -59, -78, -82, -76, -23,-107, -37, -50,
            -11,  20,  35, -42, -39,  31,   2, -22,
                -9,  39, -32,  41,  52, -10,  28, -14,
                25,  17,  20,  34,  26,  25,  15,  10,
                13,  10,  17,  23,  17,  16,   0,   7,
                14,  25,  24,  15,   8,  25,  20,  15,
                19,  20,  11,   6,   7,   6,  20,  16,
                -7,   2, -15, -12, -14, -15, -10, -10),
        'R': (  35,  29,  33,   4,  37,  33,  56,  50,
                55,  29,  56,  67,  55,  62,  34,  60,
                19,  35,  28,  33,  45,  27,  25,  15,
                0,   5,  16,  13,  18,  -4,  -9,  -6,
            -28, -35, -16, -21, -13, -29, -46, -30,
            -42, -28, -42, -25, -25, -35, -26, -46,
            -53, -38, -31, -26, -29, -43, -44, -53,
            -30, -24, -18,   5,  -2, -18, -31, -32),
        'Q': (   6,   1,  -8,-104,  69,  24,  88,  26,
                14,  32,  60, -10,  20,  76,  57,  24,
                -2,  43,  32,  60,  72,  63,  43,   2,
                1, -16,  22,  17,  25,  20, -13,  -6,
            -14, -15,  -2,  -5,  -1, -10, -20, -22,
            -30,  -6, -13, -11, -16, -11, -16, -27,
            -36, -18,   0, -19, -15, -15, -21, -38,
            -39, -30, -31, -13, -31, -36, -34, -42),
        'K': (   4,  54,  47, -99, -99,  60,  83, -62,
            -32,  10,  55,  56,  56,  55,  10,   3,
            -62,  12, -57,  44, -67,  28,  37, -31,
            -55,  50,  11,  -4, -19,  13,   0, -49,
            -55, -43, -52, -28, -51, -47,  -8, -50,
            -47, -42, -43, -79, -64, -32, -29, -32,
                -4,   3, -14, -50, -57, -18,  13,   4,
                17,  30,  -3, -14,   6,  -1,  40,  18),
        }

    A1, H1, A8, H8 = 91, 98, 21, 28
    N, E, S, W = -10, 1, 10, -1
    directions = {
        'P': (N, N+N, N+W, N+E),
        'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
        'B': (N+E, S+E, S+W, N+W),
        'R': (N, E, S, W),
        'Q': (N, E, S, W, N+E, S+E, S+W, N+W),
        'K': (N, E, S, W, N+E, S+E, S+W, N+W)
    }

    def gen_moves(self):
        for i, p in enumerate(self.board):
            if not p.isupper():
                continue
            for d in Location.directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    if q.isspace() or q.isupper():
                        break
                    if p == 'P' and d in (Location.N, Location.N+Location.N) and q != '.':
                        break
                    if p == 'P' and d in (Location.N+Location.W, Location.N+Location.E) and q == '.' and j not in (self.ep, self.kp, self.kp-1, self.kp+1):
                        break
                    yield (i, j)
                    if p in 'PNK' or q.islower():
                        break
                    if i == Location.A1 and self.board[j+Location.E] == 'K' and self.wc[0]:
                        yield (j+Location.E, j+Location.W)
                    if i == Location.H1 and self.board[j+Location.W] == 'K' and self.wc[1]:
                        yield (j+Location.W, j+Location.E)

    def rotate(self):
        return Location(self.board[::-1].swapcase(), -self.score, self.bc, self.wc, 119-self.ep if self.ep else 0, 119-self.kp if self.kp else 0)

    def nullmove(self):
        return Location(self.board[::-1].swapcase(), -self.score, self.bc, self.wc, 0, 0)

    def setBoard(self, board):
        return Location(board, self.score, self.bc, self.wc, 0, 0)

    def move(self, pos):
        i, j = pos
        p, q = self.board[i], self.board[j]
        put = lambda board, i, p: board[:i] + p + board[i+1:]
        board = self.board
        wc, bc, ep, kp = self.wc, self.bc, 0, 0
        score = self.score + self.value(pos)
        board = put(board, j, board[i])
        board = put(board, i, '.')
        if i == Location.A1:
            wc = (False, wc[1])
        if i == Location.H1:
            wc = (wc[0], False)
        if j == Location.A8:
            bc = (bc[0], False)
        if j == Location.H8:
            bc = (False, bc[1])
        if p == 'K':
            wc = (False, False)
            if abs(j-i) == 2:
                kp = (i+j)//2
                board = put(board, Location.A1 if j < i else Location.H1, '.')
                board = put(board, kp, 'R')
        if p == 'P':
            if Location.A8 <= j <= Location.H8:
                board = put(board, j, 'Q')
            if j-i == 2*Location.N:
                ep = i+Location.N
            if j == self.ep:
                board = put(board, j+Location.S, '.')
        
        return Location(board, score, wc, bc, ep, kp).rotate()

    def value(self, pos):
        i, j = pos
        p, q = self.board[i], self.board[j]
        score = Location.pst[p][j] - Location.pst[p][i]
        if q.islower():
            score += Location.pst[q.upper()][119-j]
        if abs(j-self.kp) < 2:
            score += Location.pst['K'][119-j]
        if p == 'K' and abs(i-j) == 2:
            score += Location.pst['R'][(i+j)//2]
            score -= Location.pst['R'][Location.A1 if j < i else Location.H1]
        if p == 'P':
            if Location.A8 <= j <= Location.H8:
                score += Location.pst['Q'][j] - Location.pst['P'][j]
            if j == self.ep:
                score += Location.pst['P'][119-(j+Location.S)]
        return score
