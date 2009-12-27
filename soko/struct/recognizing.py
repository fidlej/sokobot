
from soko.mazing import Maze
from soko.env.coding import PLAYER_MARKS, UNKNOWN_MARK
from pylib import v2

class Gate(object):
    """A represetation of an local aggregate state.
    """
    def __init__(self, end_states, pattern):
        self.end_states = end_states
        self.pattern = pattern

    def get_norm_pattern(self):
        """Returns a pattern to represent
        the gate input in a normalized state.
        """
        return self.pattern

    def get_end_states(self):
        """Returns the end states from this gate.
        They are represented as actions relative to the gate position.
        """
        return self.end_states

    def __eq__(self, other):
        return self.end_states == other.end_states


class PatternRecognizer(object):
    def __init__(self, endings):
        self.endings = endings

    def recognize_gates(self, s):
        """Returns a list of (pos, gate) pairs.
        They are the recognized the local aggregate states and theirs positions.
        """
        #TODO: support any env
        maze = Maze(s)
        positions = maze.find_all_positions(PLAYER_MARKS)
        gates = []
        for pos in positions:
            #TODO: Allow the local state to be uknown.
            shifted_gate = self._find_gate(maze, pos)
            gates.append(shifted_gate)

        return gates

    def _find_gate(self, maze, pos):
        shift, ending = self._find_ending(maze, pos)
        end_states, patterns = ending
        return (shift, Gate(end_states,
            self._choose_normalizing_pattern(patterns)))

    def _choose_normalizing_pattern(self, patterns):
        if patterns:
            return patterns[0]
        return ()

    def _find_ending(self, maze, pos):
        """Returns the ending matching the given
        maze with the given focus position.
        The patterns are tested in their predefined order.
        """
        for ending in self.endings:
            end_states, patterns = ending
            for pattern in patterns:
                local_maze = Maze(pattern)
                local_positions = local_maze.find_all_positions(PLAYER_MARKS)
                for local_pos in local_positions:
                    shift = v2.diff(pos, local_pos)
                    if _is_matching(shift, pattern, maze):
                        return (shift, ending)

        #TODO: report the unseen patterns
        return ((0,0), ((), ()))
        print maze
        assert None is "Impossible for now."

def _is_matching(shift, pattern, maze):
    for y, row in enumerate(pattern):
        for x, mark in enumerate(row):
            if mark == UNKNOWN_MARK:
                continue

            pos = v2.sum(shift, (x,y))
            try:
                if mark != maze.get(pos):
                    return False
            except IndexError, e:
                return False

    return True

