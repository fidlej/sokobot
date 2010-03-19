
import math
from nose.tools import assert_equal

from soko.solver import mc

class Fake:
    def choice(self, weights):
        self.weights = weights

def test_softmax():
    fake = Fake()
    mc._weighted_choice = fake.choice
    weights = [0.5, 0.0, 0.8]
    mc._softmax([w + 1000 for w in weights])

    expected_weights = [math.exp(w/0.1) for w in weights]
    _assert_floats(_normalize(fake.weights), _normalize(expected_weights))

def _assert_floats(got, expected):
    for a, b in zip(got, expected):
        assert_equal("%.7f" % a, "%.7f" % b)

def _normalize(weights):
    total = float(sum(weights))
    return [w/total for w in weights]

