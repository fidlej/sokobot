
from soko.env.coding import UNKNOWN_MARK
from soko.struct.recognizing import Gate
from soko.struct import modeling

class ExpanderBasedRecognizer(object):
    def __init__(self, expander):
        self.expander = expander
    def recognize_gates(self, s):
        """Returns a list of (pos, gate) pairs.
        """
        _report_seen_context(s)

        end_states = []
        for a in self.expander.get_actions(s):
            next_s = modeling.predict(s, a)
            end_states.append(next_s)

        gate = Gate(end_states)
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
            slice = [unknown_value] * -start + slice
        else:
            slice = list(array[start:end+1])

        if end >= len(array):
            slice += [unknown_value] * (diameter - len(slice))

        assert len(slice) == diameter
        items.append(slice)
    return items

