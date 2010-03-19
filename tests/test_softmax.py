
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
    mc._softmax(weights)

    expected_weights = [math.exp(w/0.1) for w in weights]
    assert_equal(fake.weights, expected_weights)

