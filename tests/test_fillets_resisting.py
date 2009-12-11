
import unittest

from soko import mazing
from soko.env.fillets import parsing, resisting

class Test(unittest.TestCase):
    def setUp(self):
        self.maze = mazing.parse_maze("data/fillets/start.txt")
        self.models = parsing.parse_models(self.maze)
        self.field = resisting.Field(self.maze)
        self.field.place_models(self.models)

    def test_get_resist_set(self):
        small = self._model("+")

        onright = self._get_shift_resist(small, (1, 0))
        self.assertEquals(0, len(onright))

        onleft = self._get_shift_resist(small, (-1, 0))
        self.assertEquals(1, len(onleft))
        self.assertEquals(self._model("a"), onleft[0])

        below = self._get_shift_resist(small, (0, 1))
        self.assertEquals(1, len(below))
        self.assertEquals(self._model("d"), below[0])

        above = self._get_shift_resist(small, (0, -1))
        self.assertEquals(0, len(above))

        wall = self._model("#")
        above = self._get_shift_resist(wall, (0, -1))
        self.assertEquals(3, len(above))

    def x_test_get_unit_resist(self):
        small = self._model("+")

        onright = self._get_unit_shift_resist(small, (1, 0))
        self.assertEquals(0, len(onright))

        onleft = self._get_unit_shift_resist(small, (-1, 0))
        self.assertEquals(False, onleft)

        below = self._get_unit_shift_resist(small, (0, 1))
        self.assertEquals(False, below)

        above = self._get_unit_shift_resist(small, (0, -1))
        self.assertEquals(0, len(above))

        big = self._model("*")
        onright = self._get_unit_shift_resist(big, (1, 0))
        self.assertEquals(1, len(onright))

    def _get_unit_shift_resist(self, unit, shift):
        return resisting.get_unit_resist(self.field, unit, shift)

    def _get_shift_resist(self, model, shift):
        resist_set = self.field.get_resist_set(model, shift)
        return list(resist_set)

    def _model(self, mark):
        return parsing.find_model(self.models, mark)

