
from soko import INF_COST

class Estimator(object):
    def estim_cost(self, s, cost_limit=INF_COST):
        """Estimates the cost to the goal from the given state.
        """
        raise NotImplementedError
