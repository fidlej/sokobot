
from soko.env.env import Env
from soko.struct.expanders.pushexpander import PushExpander
from soko.struct.expanders.aggregateexpander import AggregateExpander
from soko.struct.estimators import sokoestimator
from soko.struct import modeling

class EnvGlue(Env):
    def __init__(self, maze):
        self.maze = maze

    def configure(self, config):
        #TODO: allow to use different classes based on the command line args
        #self.expander = PushExpander()
        self.expander = AggregateExpander()
        #self.estimator = sokoestimator.BoxCountingSokoEstimator()
        self.estimator = sokoestimator.SokoEnvSokoEstimator()
        self.estimator.setup_goal(self.maze)

    def init(self):
        return modeling.extract_state(self.maze)

    def get_actions(self, s):
        return self.expander.get_actions(s)

    def predict(self, s, a):
        return modeling.predict(s, a)

    def estim_cost(self, s, cost_limit=None):
        return self.estimator.estim_cost(s)

    def format(self, s):
        from soko.mazing import Maze
        return str(Maze(s))

