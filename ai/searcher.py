from collections import namedtuple

class Searcher:
    MATE_LOWER = 50710
    MATE_UPPER = 69290

    TABLE_SIZE = 1e7

    QS_LIMIT = 219
    EVAL_ROUGHNESS = 13
    DRAW_TEST = True

    Entry = namedtuple('Entry', 'lower upper')

    def __init__(self):
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0

    def bound(self, pos, gamma, depth, root=True):
        self.nodes += 1
        depth = max(depth, 0)
        if pos.score <= -Searcher.MATE_LOWER:
            return -Searcher.MATE_LOWER

        if Searcher.DRAW_TEST:
            if not root and pos in self.history:
                return 0

        entry = self.tp_score.get((pos, depth, root), Searcher.Entry(-Searcher.MATE_UPPER, Searcher.MATE_UPPER))
        if entry.lower >= gamma and (not root or self.tp_move.get(pos) is not None):
            return entry.lower
        if entry.upper < gamma:
            return entry.upper

        def moves():
            if depth > 0 and not root and any(c in pos.board for c in 'RBNQ'):
                yield None, -self.bound(pos.nullmove(), 1-gamma, depth-3, root=False)

            if depth == 0:
                yield None, pos.score

            killer = self.tp_move.get(pos)
            if killer and (depth > 0 or pos.value(killer) >= Searcher.QS_LIMIT):
                yield killer, -self.bound(pos.move(killer), 1-gamma, depth-1, root=False)

            for move in sorted(pos.gen_moves(), key=pos.value, reverse=True):
                if depth > 0 or pos.value(move) >= Searcher.QS_LIMIT:
                    yield move, -self.bound(pos.move(move), 1-gamma, depth-1, root=False)

        best = -Searcher.MATE_UPPER
        for move, score in moves():
            best = max(best, score)
            if best >= gamma:
                if len(self.tp_move) > Searcher.TABLE_SIZE:
                    self.tp_move.clear()
                self.tp_move[pos] = move
                break
        
        if best < gamma and best < 0 and depth > 0:
            is_dead = lambda pos: any(pos.value(m) >= Searcher.MATE_LOWER for m in pos.gen_moves())
            if all(is_dead(pos.move(m)) for m in pos.gen_moves()):
                in_check = is_dead(pos.nullmove())
                best = -Searcher.MATE_UPPER if in_check else 0

        if len(self.tp_score) > Searcher.TABLE_SIZE:
            self.tp_score.clear()
        if best >= gamma:
            self.tp_score[pos, depth, root] = Searcher.Entry(best, entry.upper)
        if best < gamma:
            self.tp_score[pos, depth, root] = Searcher.Entry(entry.lower, best)

        return best

    def search(self, pos, history=()):
        self.nodes = 0
        if Searcher.DRAW_TEST:
            self.history = set(history)
            self.tp_score.clear()

        for depth in range(1, 1000):
            lower, upper = -Searcher.MATE_UPPER, Searcher.MATE_UPPER
            while lower < upper - Searcher.EVAL_ROUGHNESS:
                gamma = (lower+upper+1)//2
                score = self.bound(pos, gamma, depth)
                if score >= gamma:
                    lower = score
                if score < gamma:
                    upper = score
            
            self.bound(pos, lower, depth)
            yield depth, self.tp_move.get(pos), self.tp_score.get((pos, depth, True)).lower