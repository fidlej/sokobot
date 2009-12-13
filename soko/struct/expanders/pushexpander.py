
from soko.mazing import Maze
from soko.env.coding import PLAYER_MARKS, BOX_MARKS, EMPTY_MARKS, TARGET_MARKS
from soko.env.env import Action
from pylib import v2

PUSH_COST = 0
MOVE_COST = 1

SHIFTS = [
        (-1,0),
        (1,0),
        (0,-1),
        (0,1),
        ]

WALKABLE_MARKS = EMPTY_MARKS + TARGET_MARKS

class PushExpander(object):
    def get_actions(self, s):
        """Returns all possible actions from the given state.
        """
        actions = []
        maze = Maze(s)
        (pos,) = maze.find_all_positions(PLAYER_MARKS)
        man_mark = maze.get(pos)
        for shift in SHIFTS:
            new_pos = v2.sum(pos, shift)
            cell = maze.get(new_pos)
            if cell in WALKABLE_MARKS:
                actions.append(_action_move(maze, pos, new_pos))
            elif cell in BOX_MARKS:
                behind_new_pos = v2.sum(new_pos, shift)
                if maze.get(behind_new_pos) in WALKABLE_MARKS:
                    actions.append(_action_push(
                        maze, pos, new_pos, behind_new_pos))

        return actions

# Marks without and with the target below them.
TARGETED_EMPTY_MARKS = (EMPTY_MARKS[0], TARGET_MARKS[0])
TARGETED_PLAYER_MARKS = (PLAYER_MARKS[0], PLAYER_MARKS[1])
TARGETED_BOX_MARKS = (BOX_MARKS[0], BOX_MARKS[1])

def _effect(maze, pos, mark_choices):
    """Describes the an effect of an action.
    The effect is desribed by a (pos, mark) pair for the given position.
    It preserves the target on the position.
    """
    cell = maze.get(pos)
    with_target = 1 if cell in TARGET_MARKS else 0
    return (pos, mark_choices[with_target])

def _action_move(maze, pos, new_pos):
    cmd = (
            _effect(maze, pos, TARGETED_EMPTY_MARKS),
            _effect(maze, new_pos, TARGETED_PLAYER_MARKS),
            )
    return Action(cmd, cost=MOVE_COST)

def _action_push(maze, pos, new_pos, behind_new_pos):
    cmd = (
            _effect(maze, pos, TARGETED_EMPTY_MARKS),
            _effect(maze, new_pos, TARGETED_PLAYER_MARKS),
            _effect(maze, behind_new_pos, TARGETED_BOX_MARKS),
            )
    cost = MOVE_COST + PUSH_COST
    return Action(cmd, cost)

