
import random
import math

from soko.solver.solver import Solver
from soko.visual.lengthvisualizer import calc_path_cost
from soko.credit.assigning import Critic
from soko.credit.fakecritic import AstarCritic, RandomCritic

MAX_NUM_VISITS = 3
VISIT_PENALTY = 10
MAX_COST = 100000

class McSolver(Solver):
    """A Nested Monte-Carlo search.
    """
    def solve(self, env):
        """Returns a solution as a list of actions.
        """
        critic = Critic()
        #critic = AstarCritic(env)
        #critic = RandomCritic()
        path = self.solve_with_critic(env, critic)
        critic.save()
        #print critic

        return path

    def solve_with_critic(self, env, critic):
        s = env.init()
        info = _SearchInfo(env, critic)
        level = 1
        num_attempts = 100
        for i in xrange(num_attempts):
            path = _nested(info, s, level)
            #path = _sample(info, s)
            if path is not None:
                return path

        return None


class _SearchInfo(object):
    def __init__(self, env, critic):
        self.env = env
        self.costs = {}
        self.critic = critic

    def update_best_cost(self, s, path):
        """Returns and stores the best known cost for the given state.
        It could return None when there seems to be no solution.
        """
        if path is None:
            return self.costs.get(s)
            return known_cost

        self._update_costs(s, path)
        return self.costs[s]

    def _update_costs(self, s, path):
        cost = calc_path_cost(path)
        self.costs[s] = min(self.costs.get(s, cost), cost)
        for a in path:
            cost -= a.get_cost()
            s = self.env.predict(s, a)
            self.costs[s] = min(self.costs.get(s, cost), cost)

class _Memory(object):
    def __init__(self):
        self.visits = {}
    def get_num_visits(self, s):
        return self.visits.get(s, 0)
    def inc_num_visits(self, s):
        self.visits[s] = self.visits.get(s, 0) + 1


def _nested(info, s, level):
    def policy(info, s, memory):
        #print info.env.format(s)
        return _choose_best_action(info, s, level, memory)

    return _sample(info, s, policy)

def _choose_best_action(info, s, level, memory):
    """Returns the best known action in the given state.
    It returns None if the problem seems unsolvable.
    """
    env = info.env
    min_cost = None
    best_action = None
    for a in env.get_actions(s):
        next_s = env.predict(s, a)
        if level == 1:
            path = _sample(info, next_s)
        else:
            path = _nested(info, next_s, level - 1)

        cost = info.update_best_cost(next_s, path)
        if cost is None:
            continue

        cost = memory.get_num_visits(next_s) * (MAX_COST + 1) + cost
        if min_cost is None or cost < min_cost:
            min_cost = cost
            best_action = a

    #print "best action:", best_action, min_cost
    return best_action


def _is_goal(env, s):
    return env.estim_cost(s) == 0

def _choose_random_action(info, s, memory):
    """Chooses a random action.
    It gives more probability to less visited next states.
    """
    env = info.env
    #print env.format(s)
    critic = info.critic
    weights = []
    actions = env.get_actions(s)
    for a in actions:
        next_s = env.predict(s, a)
        num_visits = memory.get_num_visits(next_s)
        weights.append(critic.evaluate(s, a) - VISIT_PENALTY**num_visits)

    if not weights:
        return None

    a_index = _softmax(weights)
    return actions[a_index]

def _sample(info, s, policy=_choose_random_action):
    """Returns a random path to the goal or None.
    """
    env = info.env
    critic = info.critic
    memory = _Memory()
    path = []
    state_indexes = [s]
    while not _is_goal(env, s):
        memory.inc_num_visits(s)
        a = policy(info, s, memory)
        if a is None:
            critic.punish(env, path, state_indexes)
            return None

        s = env.predict(s, a)
        if memory.get_num_visits(s) > MAX_NUM_VISITS:
            critic.punish(env, path, state_indexes)
            return None

        # Removal of cycles from the path
        try:
            s_index = state_indexes.index(s)
        except ValueError:
            path.append(a)
            state_indexes.append(s)
        else:
            del path[s_index:]
            del state_indexes[s_index +1:]

    critic.reward(env, path, state_indexes)
    return path

def _softmax(weights):
    """Returns the index of the choosen choice.
    """
    max_w = max(weights)
    softmax_weights = [math.exp(w - max_w) for w in weights]
    return _weighted_choice(softmax_weights)

def _weighted_choice(weights):
    selection = random.random() * sum(weights)
    boundary = 0
    for i, w in enumerate(weights):
        boundary += w
        if boundary >= selection:
            return i

    assert not "Wrong normalization"

