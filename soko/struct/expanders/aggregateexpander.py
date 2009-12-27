
from soko.struct.recognizing import PatternRecognizer
from soko.struct.fakerecognizing import ExpanderBasedRecognizer
from soko.struct import modeling
from soko.env.env import Action
from soko.env.coding import UNKNOWN_MARK
from pylib import v2

def _get_fake_recognizer():
    #TODO: allow to configure the used low_level_expander
    from soko.struct.expanders.pushexpander import PushExpander
    low_level_expander = PushExpander()
    return ExpanderBasedRecognizer(low_level_expander)

def _get_pattern_recognizer():
    import cPickle as pickle
    endings = pickle.load(open("../export/endings/sokoban2.pickle"))
    return PatternRecognizer(endings)

class AggregateExpander(object):
    def __init__(self):
        #TODO: allow to pass in or configure the used recognizer
        #self.recognizer = _get_fake_recognizer()
        self.recognizer = _get_pattern_recognizer()

    def get_actions(self, s):
        actions = []
        pos_gates = self.recognizer.recognize_gates(s)
        for pos, gate in pos_gates:
            for end_state in gate.get_end_states():
                next_s = _apply_end_state(s, pos, end_state)
                next_s = self._normalize_state(next_s)
                a = _prepare_action(s, next_s)
                actions.append(a)

        return actions

    def _normalize_state(self, s):
        """Converts the patterns in the state
        to their normalized form.
        """
        orig_s = s
        pos_gates = self.recognizer.recognize_gates(s)
        for pos, gate in pos_gates:
            s = _apply_end_state(s, pos, gate.get_norm_pattern())

        # The normalization should not be too aggresive.
        # It would prevent to go in some directions.
        new_gates = self.recognizer.recognize_gates(s)
        if new_gates != pos_gates:
            return orig_s
        return s

def _prepare_action(s, next_s, cost=1):
    """Returns an action that would do the transition.
    """
    cmd = []
    for y, (row, next_row) in enumerate(zip(s, next_s)):
        for x, (cell, next_cell) in enumerate(zip(row, next_row)):
            if cell != next_cell:
                change_pos = (x,y)
                cmd.append((change_pos, next_cell))

    return Action(cmd, cost)

def _apply_end_state(s, shift, end_state):
    next_s = modeling.mutablize(s)
    for local_y, row in enumerate(end_state):
        for local_x, mark in enumerate(row):
            if mark is not UNKNOWN_MARK:
                x, y = v2.sum(shift, (local_x,local_y))
                next_s[y][x] = mark

    return next_s

