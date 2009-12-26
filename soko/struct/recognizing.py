
from soko.mazing import Maze
from soko.env.coding import PLAYER_MARKS

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


class PatternRecognizer(object):
    def __init__(self, pattern_ends):
        self.pattern_ends = pattern_ends

    def recognize_gates(self, s):
        """Returns a list of (pos, gate) pairs.
        They are the recognized the local aggregate states and theirs positions.
        """
        #TODO: support any env
        maze = Maze(s)
        positions = maze.find_all_positions(PLAYER_MARKS)
        for pos in positions:
            #TODO: Allow the local state to be uknown.
            #TODO: implement
            pass




