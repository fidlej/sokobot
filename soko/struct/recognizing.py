
from soko.mazing import Maze
from soko.env.coding import PLAYER_MARKS, UNKNOWN_MARK
from pylib import v2

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

    def __eq__(self, other):
        return self.end_states == other.end_states


class PatternRecognizer(object):
    def __init__(self, endings, fallback_recognizer):
        self.endings = endings
        self.fallback_recognizer = fallback_recognizer

    def recognize_gates(self, s):
        """Returns a list of (pos, gate) pairs.
        They are the recognized the local aggregate states and theirs positions.
        """
        #TODO: support any env
        maze = Maze(s)
        positions = maze.find_all_positions(PLAYER_MARKS)
        gates = []
        for pos in positions:
            shifted_gate = self._find_gate(maze, pos)
            if shifted_gate is None:
                return self.fallback_recognizer.recognize_gates(s)

            gates.append(shifted_gate)

        return gates

    def _find_gate(self, maze, pos):
        """Returns a known matching gate or None.
        """
        shifted_ending = self._find_ending(maze, pos)
        if shifted_ending is None:
            return None

        shift, ending = shifted_ending
        end_states, patterns = ending
        return (shift, Gate(end_states))

    def _find_ending(self, maze, pos):
        """Returns the ending matching the given
        maze with the given focus position.
        It returns None when no known pattern is matching the maze.
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

        return None

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

