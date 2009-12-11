
from soko import INF_COST

class Env(object):
    def configure(self, config):
        """Allows to configure the env.
        """
        self.config = config

    def init(self):
        """Returns the initial state.
        """
        raise NotImplementedError

    def get_actions(self, s):
        """Returns a list of possible actions from the given state.
        """
        raise NotImplementedError

    def predict(self, s, a):
        """Returns the next state when taking the given action
        in the given state.
        """
        raise NotImplementedError

    def estim_cost(self, s, cost_limit=INF_COST):
        """Estimates the remaining cost to a goal.
        I.e., it computes the h(s) used by A*.
        It returns zero cost when the given state is a goal.
        """
        raise NotImplementedError

    def relax(self, s):
        """Returns a list of independed relaxed states.
        """
        return ()

    def format(self, s):
        """Returns a string representation of the state.
        """
        return str(s)


class Action(object):
    def __init__(self, cmd, cost=1):
        self.cmd = cmd
        self.cost = cost
        self.prefer = False

    def get_cmd(self):
        """Returns the internal action command.
        """
        return self.cmd

    def set_prefer(self, prefer):
        """Sets whether this action should be preferred.
        """
        self.prefer = prefer
    def is_preferred(self):
        return self.prefer

    def set_cost(self, cost):
        """Corrects the cost.
        """
        self.cost = cost
    def get_cost(self):
        """Returns the action cost.
        """
        return self.cost

    def __str__(self):
        return str(self.cmd)

