
from soko.env.env import Env
from soko.struct.expanders.pushexpander import PushExpander
from soko.struct.estimators import sokoestimator

class EnvGlue(Env):
    def __init__(self, maze):
        self.maze = maze

    def configure(self, config):
        #TODO: allow to use different classes based on the command line args
        self.expander = PushExpander()
        #self.estimator = sokoestimator.BoxCountingSokoEstimator()
        self.estimator = sokoestimator.SokoEnvSokoEstimator()
        self.estimator.setup_goal(self.maze)
        self.model = ActionModel()

    def init(self):
        field = self.maze.render_maze()
        return _immutablize(field)

    def get_actions(self, s):
        return self.expander.get_actions(s)

    def predict(self, s, a):
        return self.model.predict(s, a)

    def estim_cost(self, s, cost_limit=None):
        return self.estimator.estim_cost(s)

    def format(self, s):
        from soko.mazing import Maze
        return str(Maze(s))


def _immutablize(field):
    return tuple(tuple(line) for line in field)

def _mutablize(field):
    return list(list(line) for line in field)


class ActionModel(object):
    def predict(self, s, a):
        """Returns the next state.
        """
        next_s = _mutablize(s)
        for pos, mark in a.get_cmd():
            x, y = pos
            next_s[y][x] = mark

        return _immutablize(next_s)

