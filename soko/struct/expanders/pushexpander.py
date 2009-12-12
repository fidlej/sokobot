
from soko.mazing import Maze
from soko.env.coding import PLAYER_MARKS, BOX_MARKS, EMPTY_MARKS
from soko.env.env import Action
from pylib import v2

PUSH_COST = 0
MOVE_COST = 1

SHIFTS = [
        (0,-1),
        (1,0),
        (0,1),
        (-1,0),
        ]

class PushExpander(object):
    def get_actions(self, s):
        """Returns all possible actions from the given state.
        """
        actions = []
        maze = Maze(s)
        pos = maze.find_all_positions(PLAYER_MARKS)[0]
        for shift in SHIFTS:
            new_pos = v2.sum(pos, shift)
            cell = maze.get(new_pos)
            if cell in EMPTY_MARKS:
                actions.append(_action_move(s, pos, new_pos))
            elif cell in BOX_MARKS:
                behind_new_pos = v2.sum(new_pos, shift)
                if maze.get(behind_new_pos) in EMPTY_MARKS:
                    actions.append(_action_push(
                        s, pos, new_pos, behind_new_pos))

        return actions

def _action_move(s, pos, new_pos):
    cmd = (
            (pos, EMPTY_MARKS[0]),
            (new_pos, PLAYER_MARKS[0]),
            )
    return Action(cmd, cost=MOVE_COST)

def _action_push(s, pos, new_pos, behind_new_pos):
    cmd = (
            (pos, EMPTY_MARKS[0]),
            (new_pos, PLAYER_MARKS[0]),
            (behind_new_pos, BOX_MARKS[0]),
            )
    cost = MOVE_COST + PUSH_COST
    return Action(cmd, cost)

