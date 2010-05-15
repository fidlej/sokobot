
import math

from soko.struct.modeling import immutablize
from soko.credit.storing import Storage
from soko import formatting

MARGIN = 1
DEFAULT_CREDIT = 0.9
LEARNING_RATE = 0.5

class Critic(object):
    def __init__(self, storage_filename="../export/credit/critic.pickle"):
        self.credits = {}
        if storage_filename:
            self.storage = Storage(storage_filename)
            self.credits = self.storage.load(default=self.credits)

    def reward(self, env, actions, states):
        """Gives more credit to the given actions.
        """
        self._assign_credit(env, actions, states, 1)

    def punish(self, env, actions, states):
        self._assign_credit(env, actions, states, -1)

    def evaluate(self, s, a):
        """Returns a weight that the move is a good move.
        Bad moves should have negative weights.
        """
        return self.credits.get(_identify_move(s, a), DEFAULT_CREDIT)

    def save(self):
        self.storage.save(self.credits)

    def _assign_credit(self, env, actions, states, credit):
        """Assigns the given credit to all actions on the given path.
        """
        # It uses the REINFORCE estimation of dPolicyValue(w)/dw_i.
        # http://www.scholarpedia.org/article/Policy_gradient_methods
        #
        # The policy parameters are updated to move the policyValue uphill:
        # w_i = w_i + alpha * dPolicyValue(w)/dw_i
        # 
        # For a generic policy:
        # dPolicyValue(w)/dw_i ~= sum_k_till_Horizont(
        #   dlog(pi(s_k, a_k)/dw1
        #   ) * total_reward
        #
        #   where the correct dPolicyValue would be the expected value
        #   over many trials.
        #
        # For the softmax policy:
        # dPolicyValue(w)/dw_i ~= sum_k_till_Horizont(
        #   dQ(s_k,a_k)/dw_i - sum_a'(pi(s_k,a') * dQ(s_k, a')/d_wi)
        #   ) * total_reward
        #
        # For Q(s,a) = w_1*match_1(s,a) + w_2*match_2(s,a) + ...:
        # dQ(s,a)/dw_i = match_i(s,a)
        #
        # For having patterns that match only in one state:
        # dPolicyValue(w)/dw_i ~= (1 - pi(s,a)) * total_reward
        #   if there is (s,a) with match_i(s,a) == 1
        #   else 0

        for s, a in zip(states, actions):
            pi = self._calc_softmax_prob(env, s, a)
            gradient = (1 - pi) * credit
            move = _identify_move(s, a)
            self.credits.setdefault(move, DEFAULT_CREDIT)
            self.credits[move] += LEARNING_RATE * gradient

    def _calc_softmax_prob(self, env, s, a):
        """Returns the probability of the given (s,a) pair
        under the softmax policy.
        """
        weights = [self.evaluate(s, other) for other in env.get_actions(s)]
        a_w = self.evaluate(s, a)
        max_w = max(weights)
        pi = math.exp(a_w - max_w) / sum(math.exp(w - max_w) for w in weights)
        assert 0.0 <= pi <= 1.0
        return pi

    def __str__(self):
        output = ""
        pairs = [(credit, move) for move, credit in self.credits.iteritems()]
        pairs.sort()
        for credit, move in pairs:
            output += "%s %s" % (Move(move), credit)
        output += "unique_moves: %s" % len(pairs)
        return output


class Move(object):
    def __init__(self, pattern):
        self.pattern = pattern

    def __eq__(self, other):
        return self.pattern == other.pattern

    def __hash__(self):
        return hash(self.pattern)

    def __str__(self):
        return formatting.stringify(self.pattern)

def _identify_move(s, a):
    #TODO: ignore non-struct states and actions
    pattern = []
    effects = a.get_cmd()
    xs = [pos[0] for pos, mark in effects]
    ys = [pos[1] for pos, mark in effects]
    min_x = min(xs)
    max_x = max(xs)
    for y in xrange(min(ys) - MARGIN, max(ys) + MARGIN + 1):
        row = s[y]
        pattern_row = []
        pattern.append(pattern_row)
        for x in xrange(min_x - MARGIN, max_x + MARGIN + 1):
            pattern_row.append(row[x])

    return immutablize(pattern)

