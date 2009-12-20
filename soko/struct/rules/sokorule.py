
from soko.env.coding import PLAYER_MARKS, BOX_MARKS, UNKNOWN_MARK
from soko.struct.expanders.pushexpander import PushExpander, SHIFTS
from soko.struct import modeling
from soko.mazing import Maze
from pylib import v2

class PushRule(object):
    def __init__(self):
        self.expander = PushExpander()

    def get_children(self, s, used_cells):
        """Returns the children for the given local state
        or None if it is an end state of its pattern.

        When some children are returned, the set of used cells will be updated
        with the cells that provided an information.
        """
        local_used_cells = self._get_used_cells(s)
        maze = Maze(s, border=UNKNOWN_MARK)
        for pos in local_used_cells:
            if maze.get(pos) == UNKNOWN_MARK:
                return None

        children = []
        actions = self.expander.get_actions(s)
        for a in actions:
            children.append(modeling.predict(s, a))

        used_cells.update(local_used_cells)
        return children

    def _get_used_cells(self, s):
        """Returns positions that are needed
        to decide if the actions are applicable in the state.
        """
        used_cells = set()
        maze = Maze(s, border=UNKNOWN_MARK)
        positions = maze.find_all_positions(PLAYER_MARKS)
        for pos in positions:
            used_cells.add(pos)
            for shift in SHIFTS:
                next_pos = v2.sum(pos, shift)
                used_cells.add(next_pos)
                if maze.get(next_pos) in BOX_MARKS:
                    next_next_pos = v2.sum(next_pos, shift)
                    used_cells.add(next_next_pos)

        return used_cells


SOKOBAN_RULES = [
        PushRule(),
        #TODO: implement the SokobanGoalRule
        #SokobanGoalRule(),
        ]
