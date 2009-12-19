
from soko.struct import modeling
from soko.env.env import Action
from pylib import v2

UNKNOWN_MARK = "%"

class AggregateExpander(object):
    def get_actions(self, s):
        actions = []
        pos_gates = _recognize_gates(s)
        for pos, gate in pos_gates:
            for local_action in gate.get_end_states():
                a = _normalize_action(s, pos, local_action)
                actions.append(a)

        return actions

class Gate(object):
    """A represetation of an local aggregate state.
    """
    def __init__(self, end_states):
        self.end_states = end_states
    def get_end_states(self):
        """Returns the end states from this gate.
        They are represented as actions relative to the gate position.
        """
        return self.end_states

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

def _recognize_gates(s):
    """Returns a list (pos, gate) pairs.
    They are the recognized the local aggregate states and theirs positions.
    """
    _report_seen_context(s)
    #TODO: implement a recognition of the gates
    from soko.struct.expanders.pushexpander import PushExpander
    expander = PushExpander()
    gate = Gate(expander.get_actions(s))
    return [((0,0), gate)]

def _report_seen_context(s):
    """Prints all seen NxM local views.
    """
    DX = 5
    DY = 5
    from soko.mazing import Maze
    from soko.env.coding import PLAYER_MARKS
    maze = Maze(s)
    man_positions = maze.find_all_positions(PLAYER_MARKS)

    unknown_row = UNKNOWN_MARK * DX
    separator = "=" * DX
    for pos in man_positions:
        x, y = pos
        for rows_view in _get_shifted_views(s, y, DY, unknown_row):
            # The row_cols_views contains a list of col views
            # for each row.
            row_cols_views = [_get_shifted_views(row, x, DX, UNKNOWN_MARK)
                    for row in rows_view if row]

            # A context is a set of cols views from all rows.
            for context in zip(*row_cols_views):
                print separator
                print Maze(context)

def _get_shifted_views(array, index, diameter, unknown_value=None):
    """Returns all slices with the given diameter.
    They have to contain the given index on a non-border position:
    i.e., on positions 1 to (slice_len - 2).
    """
    items = []
    for shift in xrange(1, (diameter - 2) + 1):
        start = index - shift
        end = index - shift + diameter - 1
        if start < 0:
            slice = list(array[0:end+1])
            slice = [unknown_value] * (diameter - len(slice)) + slice
        elif end >= len(array):
            slice = list(array[start:len(array)])
            slice += [unknown_value] * (diameter - len(slice))
        else:
            slice = array[start:end+1]
            assert len(slice) == diameter
        items.append(slice)
    return items

