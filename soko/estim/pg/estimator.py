
from soko import INF_COST
from soko.estim.estim import Estimator

class GraphPlanEstimator(Estimator):
    def __init__(self, extender):
        self.extender = extender
        self.prefer_ops = {}

    def estim_cost(self, s, cost_limit=None):
        planner = GraphPlanner(self.extender)
        graph, goal = planner.plan_graph(s)
        if goal is None:
            cost = INF_COST
        else:
            plan = _extract_plan(graph, goal)
            cost = _calc_seq_cost(plan)
            if len(plan) > 0:
                self.prefer_ops[s] = _get_prefer_ops(plan)
        return cost

    def get_prefer_ops(self, s):
        return self.prefer_ops.get(s, ())


def _extract_plan(graph, goal):
    """Extracts a relaxed plan
    from the given planning graph.
    """
    level_actions = []
    next_needed = set(goal)
    last_level = graph.get_last_level()
    for level in range(last_level, 0, -1):
        level_actions.append([])
        needed = next_needed
        next_needed = set()
        while len(needed) > 0:
            value, var = needed.pop()
            if graph.get_level(value, var) < level:
                # Using NOOP action.
                next_needed.add((value, var))
                continue

            action = graph.get_suitable_action(level, value, var)
            for effect in action.get_effects():
                needed.discard(effect)
            next_needed.update(action.get_pres())
            level_actions[-1].append(action)

        level_actions[-1].reverse()

    level_actions.reverse()
    return level_actions

def _calc_seq_cost(level_actions):
    cost = 0
    for actions in level_actions:
        cost += len(actions)
    return cost

def _get_prefer_ops(level_actions):
    """Extracts the preferred operators.
    It prefers all actions available from the start state
    of the relaxed plan.
    """
    return level_actions[0]


class GraphPlanner(object):
    def __init__(self, extender):
        self.extender = extender

    def plan_graph(self, s):
        start_effects = self.extender.reset(s)
        reach = Reach()
        reach.extend_reach(start_effects)
        graph = PlanningGraph(reach)

        reachable = reach.get_reachable()
        reached_goal = self.extender.get_reached_goal(s, reachable)
        while not reached_goal:
            new_values = reach.get_new_values()
            actions = self.extender.get_new_actions(reachable, new_values)
            if len(actions) == 0:
                return None, None

            graph.add_layer(actions)
            reachable = reach.get_reachable()
            reached_goal = self.extender.get_reached_goal(s, reachable)

        return graph, reached_goal


class PlanningGraph(object):
    def __init__(self, reach):
        self.layers = []
        self.reach = reach

    def add_layer(self, actions):
        self.layers.append(actions)
        self.reach.inc_level()
        for a in actions:
            self.reach.extend_reach(a.get_effects())

    def get_last_level(self):
        """Returns the last index of the proposition layer.
        """
        # proposition_layer_index == action_layer_index + 1
        return len(self.layers)

    def get_level(self, value, var):
        """Returns the first proposition level where var=value was reached.
        """
        return self.reach.get_level(value, var)

    def get_suitable_action(self, level, value, var):
        """Returns an action to reach var=value in the given level.
        """
        #TODO: optimize
        #TODO: consider the difficulties of the actions
        needed_effect = (value, var)
        action_level = level - 1
        for action in self.layers[action_level]:
            for effect in action.get_effects():
                if effect == needed_effect:
                    return action

        raise Exception("Invalid request, no such action: %s, %s, %s"
                % (level, value, var))


class Reach(object):
    def __init__(self):
        self.level = 0
        self.variables = {}
        self.new_values = []
        self.reachable = Reachable(self)

    def inc_level(self):
        self.level += 1
        self.new_values = []

    def get_new_values(self):
        return self.new_values

    def get_reachable(self):
        return self.reachable

    def extend_reach(self, effects):
        for value, var in effects:
            var_set = self.variables.setdefault(var, {})
            if value not in var_set:
                var_set[value] = self.level
                self.new_values.append((value, var))

    def get_level(self, value, var):
        """Returns the first level where var=value was reached.
        Returns None when it wasn't reached yet.
        """
        var_set = self.variables.get(var)
        if var_set is None:
            return None
        return var_set.get(value)

class Reachable(object):
    def __init__(self, reach):
        self.reach = reach
    def is_in(self, val, tile):
        return self.reach.get_level(val, tile) is not None

