
import unittest

from soko import mazing
from soko.env import npuzzle
from soko.env.env import Action

class Test(unittest.TestCase):
    def setUp(self):
        maze = mazing.Maze([
            "1234",
            "5678",
            "9ab~",
            ])
        self.env = npuzzle.PuzzleEnv(maze)
        self.s = self.env.init()

    def test_replace(self):
        row = tuple("0123")
        self.assertEquals(tuple("01~3"), npuzzle._replace(row, 2, "~"))

    def test_get_actions(self):
        actions = self.env.get_actions(self.s)
        cmds = [a.get_cmd() for a in actions]
        self.assertEquals([(-1,0), (0,-1)], cmds)

    def test_predict(self):
        new_s = self.env.predict(self.s, Action((-1,0)))
        self.assertEquals((
            tuple("1234"),
            tuple("5678"),
            tuple("9a~b"),
            ), new_s)

        new_s = self.env.predict(self.s, Action((0,-1)))
        self.assertEquals((
            tuple("1234"),
            tuple("567~"),
            tuple("9ab8"),
            ), new_s)

    def test_estim_cost(self):
        self.assertEquals(0, self.env.estim_cost(self.s))
        new_s = self.env.predict(self.s, Action((-1,0)))
        self.assertTrue(new_s != self.s)
        self.assertEquals(1, self.env.estim_cost(new_s))

