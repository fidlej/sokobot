
from soko.struct.modeling import immutablize

MARGIN = 1

class Critic(object):
    def __init__(self):
        self.credits = {}

    def reward(self, actions, states):
        """Gives more credit to the given actions.
        """
        self._assign_credit(actions, states, 1)

    def punish(self, actions, states):
        self._assign_credit(actions, states, -1)

    def _assign_credit(self, actions, states, credit):
        if len(actions) == 0:
            return

        partial_credit = credit/float(len(actions))
        for move in _get_moves(states, actions):
            self.credits[move] = self.credits.get(move, 0) + partial_credit


def _get_moves(states, actions):
    moves = []
    for s, a in zip(states, actions):
        move = _identify_move(s, a)
        moves.append(move)
    return moves

def _identify_move(s, a):
    #TODO: ignore non-struct states and actions
    pattern = []
    effects = a.get_cmd()
    xs = [pos[0] for pos, mark in effects]
    ys = [pos[1] for pos, mark in effects]
    min_x = min(xs)
    max_x = max(xs)
    for y in xrange(min(ys) - MARGIN, max(ys) + MARGIN + 1):
        row = s[y]
        pattern_row = []
        pattern.append(pattern_row)
        for x in xrange(min_x - MARGIN, max_x + MARGIN + 1):
            pattern_row.append(row[x])

    return immutablize(pattern)

