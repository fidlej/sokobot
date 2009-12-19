
from soko.mazing import Maze
from soko.env.env import Action

SPACE_MARK = "_"
LEFT_FROG_MARK = ">"
RIGHT_FROG_MARK = "<"

class FrogExpander(object):
    def get_actions(self, s):
        actions = []
        maze = Maze(s)
        (pos,) = maze.find_positions(SPACE_MARK)
        actions += _find_possible_actions(maze, pos, xrange(-2, -1+1),
                LEFT_FROG_MARK)
        actions += _find_possible_actions(maze, pos, xrange(1, 2+1),
                RIGHT_FROG_MARK)

        return actions

class FrogEstimator(object):
    def setup_goal(self, maze):
        pass
    def estim_cost(self, s):
        """All left frogs has to be on the right side
        and the right frogs on the left size.
        """
        assert len(s) == 1
        width = len(s[0])
        maze = Maze(s)
        right_frogs = maze.find_positions(RIGHT_FROG_MARK)
        for pos in right_frogs:
            x, y = pos
            if x >= len(right_frogs):
                return 1

        left_frogs = maze.find_positions(LEFT_FROG_MARK)
        for pos in left_frogs:
            x, y = pos
            if x < width - len(left_frogs):
                return 1

        return 0


def _find_possible_actions(maze, pos, shifts, frog_mark):
    actions = []
    for new_pos in _find_ready_frogs(maze, pos, shifts, frog_mark):
        actions.append(_action_jump(pos, new_pos, frog_mark))
    return actions

def _find_ready_frogs(maze, pos, shifts, frog_mark):
    ready_positions = []
    x, y = pos
    width = len(maze.render_maze()[0])
    for shift in shifts:
        new_x = x + shift
        if new_x < 0 or new_x >= width:
            continue

        new_pos = (new_x, y)
        cell = maze.get(new_pos)
        if cell == frog_mark:
            ready_positions.append(new_pos)
    return ready_positions


def _action_jump(pos, new_pos, frog_mark):
    cmd = (
            (pos, frog_mark),
            (new_pos, SPACE_MARK),
            )
    return Action(cmd)

