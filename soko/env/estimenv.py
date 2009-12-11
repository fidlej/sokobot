
from soko import INF_COST
from soko.estim.pg import extender_pusher, estimator

class EstimPgEnv(object):
    def __init__(self, env):
        self.env = env
        #TODO: support not just Sokoban and pusher
        if hasattr(env, "get_targets"):
            extender = extender_pusher.SokobanExtender(env)
        else:
            extender = extender_pusher.PusherExtender(env)
        self.estimator = estimator.GraphPlanEstimator(extender)

    def estim_cost(self, s, cost_limit=INF_COST):
        cost = self.estimator.estim_cost(s, cost_limit)
        if cost == 0:
            cost = self.env.estim_cost(s, cost_limit)
        return cost

    def get_actions(self, s):
        #TODO: support not just pusher envs
        preferred_ops = self.estimator.get_prefer_ops(s)
        preferred_shifts = [_extract_shift(op) for op in preferred_ops]
        action_shifts = self.env.path_env.action_shifts

        actions = self.env.get_actions(s)
        for a in actions:
            if action_shifts[a.get_cmd()] in preferred_shifts:
                a.set_prefer(True)

        return actions

    def __getattr__(self, name):
        return getattr(self.env, name)

def _extract_shift(operator):
    from pylib import v2
    orig = _find_tile(operator.get_pres(), 'x')
    new = _find_tile(operator.get_effects(), 'x')
    return v2.diff(new, orig)

def _find_tile(facts, value):
    for fact_value, var in facts:
        if value == fact_value:
            return var
    raise KeyError("No tile for %r in: %s" % (value, facts))

