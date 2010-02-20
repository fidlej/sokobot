
from soko.struct.modeling import immutablize
from soko.credit.storing import Storage

MARGIN = 1
DEFAULT_CREDIT = 0
DEFAULT_ENTRY = (DEFAULT_CREDIT, 0)

class Critic(object):
    def __init__(self):
        self.storage = Storage("../export/credit/critic.pickle")
        self.credits = self.storage.load(default={})

    def reward(self, actions, states):
        """Gives more credit to the given actions.
        """
        self._assign_credit(actions, states, 1)

    def punish(self, actions, states):
        if len(actions) == 0:
            return
        p_bad = 1.0/len(actions)
        self._assign_credit(actions, states, -1*p_bad)

    def evaluate(self, s, a):
        """Returns a weight that the move is a good move.
        """
        total, num_uses = self.credits.get(_identify_move(s, a), DEFAULT_ENTRY)
        if num_uses == 0:
            return DEFAULT_CREDIT
        return total/float(num_uses)

    def save(self):
        self.storage.save(self.credits)

    def _assign_credit(self, actions, states, credit):
        """Assigns the given credit to all actions on the given path.
        """
        for move in _get_moves(states, actions):
            total, num_uses = self.credits.get(move, DEFAULT_ENTRY)
            self.credits[move] = (total + credit, num_uses + 1)


def _get_moves(states, actions):
    moves = []
    for s, a in zip(states, actions):
        move = _identify_move(s, a)
        moves.append(move)
    return moves


class Move(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return self.pattern == other.pattern

    def __hash__(self):
        return hash(self.pattern)

    def __str__(self):
        rows = []
        for row in self.pattern:
            rows.append("".join(row))
        return "\n".join(rows)

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

