
import unittest

from soko.estim.pg import extender, extender_pusher, estimator
from soko.env import env_lookup

class Test(unittest.TestCase):
    def setUp(self):
        level_filename = "data/sokoban/microban/level001.txt"
        self.env = env_lookup.create_env(level_filename)
        self.extender = extender_pusher.SokobanExtender(self.env)
        self.reach = estimator.Reach()
        self.reachable = self.reach.get_reachable()
        self.start_s = self.env.init()

    def test_toeffects(self):
        effects = self.extender.reset(self.start_s)
        self.assertEquals(14, len(effects))
        self.assertEquals([(2, 3)], _find_tiles('x', effects))
        self.assertEquals(1, len(_find_tiles('o0', effects)))
        self.assertEquals(1, len(_find_tiles('o1', effects)))
        self.assertEquals(11, len(_find_tiles('.', effects)))

    def test_get_reached_goal(self):
        goal = self.extender.get_reached_goal(self.start_s, self.reachable)
        self.assertEquals(None, goal)

        effects = self.extender.reset(self.start_s)
        self.reach.extend_reach(effects)
        goal = self.extender.get_reached_goal(self.start_s, self.reachable)
        self.assertEquals(None, goal)

        self.assertEquals(True, self.reachable.is_in('x', (2,3)))
        self.assertEquals(False, self.reachable.is_in('x', (1,3)))
        self.assertEquals(True, self.reachable.is_in('.', (1,1)))
        self.assertEquals(False, self.reachable.is_in('.', (0,0)))

        extra_effects = [('o1', (2,1))]
        self.reach.extend_reach(extra_effects)
        goal = self.extender.get_reached_goal(self.start_s, self.reachable)
        self.assertTrue(goal is not None)
        self.assertEquals([('o1', (2,1)), ('o0', (1,3))], goal)

    def test_assign_boxes(self):
        boxvals = extender_pusher._get_boxvals(3)
        targets = (0, 1, 2)
        def fake_is_in(value, var):
            return True
        fake_is_in.is_in = fake_is_in
        goal = extender_pusher._assign_boxes(boxvals, targets, fake_is_in)
        self.assertEquals([('o2', 2), ('o1', 1), ('o0', 0)], goal)

def _find_tiles(value, effects):
    tiles = []
    for val, tile in effects:
        if val == value:
            tiles.append(tile)

    tiles.sort()
    return tiles

