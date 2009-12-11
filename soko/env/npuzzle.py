
from soko.formatting import OutputField
from soko.env.env import Env, Action
from pylib import v2

# The tilde is used because ord('~') > ord('z').
# The ord() is used in estim_cost().
SPACE_MARK = "~"

class PuzzleEnv(Env):
    def __init__(self, maze):
        self.maze = maze

    def init(self):
        field = self.maze.render_maze()
        return tuple(tuple(row) for row in field)

    def get_actions(self, s):
        x, y = self._find_space(s)
        w = len(s[0])
        h = len(s)
        actions = []
        if x > 0:
            actions.append(Action((-1,0)))
        if x < w - 1:
            actions.append(Action((1,0)))
        if y > 0:
            actions.append(Action((0,-1)))
        if y < h - 1:
            actions.append(Action((0,1)))
        return actions

    def _find_space(self, s):
        for y, row in enumerate(s):
            for x, cell in enumerate(row):
                if cell == SPACE_MARK:
                    return x, y

        raise ValueError("No space in: %r" % s)

    def predict(self, s, a):
        shift = a.get_cmd()
        space_pos = self._find_space(s)
        new_pos = v2.sum(space_pos, shift)
        return _exchange(s, space_pos, new_pos)

    def estim_cost(self, s, cost_limit=None):
        """A blind heuristic.
        It checks that the cells are sorted.
        """
        prev = 0
        for row in s:
            for cell in row:
                if ord(cell) < prev:
                    return 1
                prev = ord(cell)

        return 0

    def format(self, s):
        rows = []
        for row in s:
            rows.append(''.join(row))
        return "\n".join(rows)


def _exchange(s, apos, bpos):
    ax, ay = apos
    bx, by = bpos
    rows = []
    for i, row in enumerate(s):
        if i == ay:
            row = _replace(row, ax, s[by][bx])
        if i == by:
            row = _replace(row, bx, s[ay][ax])
        rows.append(row)

    return tuple(rows)

def _replace(row, x, mark):
    """Replaces the char at the given position in the row.
    Returns the new changed row.
    """
    row = list(row)
    row[x] = mark
    return tuple(row)

