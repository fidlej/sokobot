
from soko.runtime import suppress_logging

class AstarCritic(object):
    def __init__(self, env):
        from soko.solver import solver_lookup
        env, solver = solver_lookup.create_task(env, "astar,hweight=2")
        self.env = env
        self.solver = solver
        self.cache = {}

    def reward(self, actions, states):
        pass

    def punish(self, actions, states):
        pass

    def save(self):
        pass

    @suppress_logging
    def evaluate(self, s, a):
        """Returns 1.0 if the move leads to a solvable state.
        """
        next_s = self.env.predict(s, a)
        result = self.cache.get(next_s)
        if result is not None:
            return result

        path = self.solver.solve(self.env, next_s)
        if path is None:
            result = 0.0
        else:
            result = 1.0

        self.cache[next_s] = result
        return result
