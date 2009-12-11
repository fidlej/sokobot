
from soko.formatting import OutputField
from soko.env.env import Env, Action
from soko.env.coding import PLAYER_MARKS, WALL_MARKS, TARGET_MARKS

LEFT, RIGHT, UP, DOWN = COMMANDS = tuple(range(4))

class PathFinderEnv(Env):
    def __init__(self, maze):
        self.maze = maze
        self.action_shifts = ((-1,0), (1,0), (0,-1), (0,1))
        self.goals = self.maze.find_all_positions(TARGET_MARKS)

    def init(self):
        (pos,) = self.maze.find_all_positions(PLAYER_MARKS)
        return pos

    def get_actions(self, pos):
        transitions = self.get_near_transitions(pos)
        actions = []
        for cell_pos, a in transitions:
            if self.maze.get(cell_pos) not in WALL_MARKS:
                actions.append(a)
        return actions

    def get_near_transitions(self, pos):
        """Returns a list of near (next_s, a) pairs.
        """
        x, y = pos
        neighbors = [(x + sx, y + sy) for sx, sy in self.action_shifts]
        return zip(neighbors, [Action(cmd) for cmd in COMMANDS])

    def predict(self, pos, a):
        sx, sy = self.action_shifts[a.get_cmd()]
        x, y = pos
        return (x + sx, y + sy)

    def estim_cost(self, pos, cost_limit=None):
        x, y = pos
        min_distance = None
        for goal_pos in self.goals:
            goal_x, goal_y = goal_pos
            dx = abs(goal_x - x)
            dy = abs(goal_y - y)
            distance = dx + dy
            if min_distance is None or distance < min_distance:
                min_distance = distance

        return min_distance

    def get_goals(self):
        return self.goals

    def format(self, s):
        field = OutputField(self.maze)
        field.place_targets(self.goals)
        field.place_player(s)
        return str(field)

