
class Expander(object):
    def get_actions(self, s):
        """Returns the possible actions from the given state.
        """
        raise NotImplementedError

class Estimator(object):
    def setup_goal(self, maze):
        """Allows the estimator to know what is the goal
        before asking it for an estimation.
        """
        raise NotImplementedError

    def estim_cost(self, s):
        """Estimates the distance to the goal from the given state.
        """
        raise NotImplementedError
