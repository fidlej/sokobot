
class Solver(object):
    def solve(self, env):
        """Returns action path to the goal.
        Returns None when no such path exists.
        """
        raise NotImplementedError

    def configure(self, config):
        """Allows to configure the solver.
        """
        self.config = config
