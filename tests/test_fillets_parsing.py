
import unittest

from soko import mazing
from soko.env.fillets import parsing

class Test(unittest.TestCase):
    def test_parse_models(self):
        maze = mazing.parse_maze("data/fillets/start.txt")
        models = parsing.parse_models(maze)
        self.assertEquals(8, len(models))

        for model in models:
            if model.is_unit():
                if model.get_weight() == parsing.WEIGHT_LIGHT:
                    self.assertEquals(((0,0),(1,0),(2,0)), tuple(model.shape))
                else:
                    self.assertEquals((
                        (0,0),(1,0),(2,0),(3,0),
                        (0,1),(1,1),(2,1),(3,1)), tuple(model.shape))

