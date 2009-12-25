
from soko.struct import modeling
from soko.struct.fakerecognizing import ExpanderBasedRecognizer
from soko.env.env import Action
from pylib import v2

class AggregateExpander(object):
    def __init__(self):
        #TODO: allow to configure the used low_level_expander
        from soko.struct.expanders.pushexpander import PushExpander
        low_level_expander = PushExpander()
        self.recognizer = ExpanderBasedRecognizer(low_level_expander)

    def get_actions(self, s):
        actions = []
        pos_gates = self.recognizer.recognize_gates(s)
        for pos, gate in pos_gates:
            for local_action in gate.get_end_states():
                a = _normalize_action(s, pos, local_action)
                actions.append(a)

        return actions

def _normalize_action(s, pos, local_action):
    """Returns action that would
    produce an equivalent normalized state.
    """
    orig_cmd = [(v2.sum(pos, shift), value) for shift, value
        in local_action.get_cmd()]
    orig_action = Action(orig_cmd, local_action.get_cost())

    next_s = modeling.predict(s, orig_action)
    _normalize_state(next_s)
    cmd = []
    for y, (row, next_row) in enumerate(zip(s, next_s)):
        for x, (cell, next_cell) in enumerate(zip(row, next_row)):
            if cell != next_cell:
                change_pos = (x,y)
                cmd.append((change_pos, next_cell))

    return Action(cmd, orig_action.get_cost())

def _normalize_state(s):
    #TODO: discover local aggregates
    # and convert them to their normalized local state
    return s

