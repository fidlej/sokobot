
import unittest

from soko import mazing
from soko.env.fillets import parsing, ruling
from pylib import v2

class Test(unittest.TestCase):
    def setUp(self):
        self.maze = mazing.parse_maze("data/fillets/start.txt")
        self.models = parsing.parse_models(self.maze)
        self.rules = ruling.Rules(self.maze)
        self.rules.init_positions(self.models)

    def test_calc_move(self):
        small = parsing.find_model(self.models, "+")
        orig_positions = [m.pos for m in self.models]
        shift = (1,0)
        positions, cost = self.rules.calc_move(small, shift)

        self.assertEquals(orig_positions, [m.pos for m in self.models])
        self.assertTrue(positions is not None)
        self.assertTrue(positions != orig_positions)
        self.assertEquals(1, cost)

        index = orig_positions.index(small.pos)
        self.assertEquals(positions[index], v2.sum(small.pos, shift))
        positions[index] = small.pos
        self.assertEquals(orig_positions, positions)

        self.assertEquals((None, None), self.rules.calc_move(small, (0,1)))
        self.assertEquals((None, None), self.rules.calc_move(small, (-1,1)))
