
import unittest

from soko import mazing
from soko.env.fillets import parsing, resisting, fall
from pylib import v2

class Test(unittest.TestCase):
    def setUp(self):
        self.maze = mazing.parse_maze("data/fillets/start.txt")
        self.models = parsing.parse_models(self.maze)
        self.field = resisting.Field(self.maze)
        self.field.place_models(self.models)
        self.landslip = fall.Landslip(self.field, self.models)

    def test_find_immovable(self):
        immovable = self.landslip._find_immovable()
        self.assertEquals(3, len(immovable))
        small = parsing.find_model(self.models, "+")
        big = parsing.find_model(self.models, "*")
        wall = parsing.find_model(self.models, "#")

        self.assertTrue(small in immovable)
        self.assertTrue(big in immovable)
        self.assertTrue(wall in immovable)

    def test_get_falling(self):
        steel = parsing.find_model(self.models, "A")

        for i in range(10):
            falling = self.landslip.get_falling()
            self.assertEquals(1, len(falling))
            self.assertEquals(steel, falling[0])

            steel.pos = v2.sum(steel.pos, (0, 1))
            self.field.place_models(self.models)

        falling = self.landslip.get_falling()
        self.assertEquals(0, len(falling))

