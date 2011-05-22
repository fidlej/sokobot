
import unittest

from soko.mazing import Maze
from soko.env import pusherenv
from soko.env.env import Action
from soko.env.pathfinder import LEFT, RIGHT, UP, DOWN

class PusherEnvTest(unittest.TestCase):
    def setUp(self):
        field = [
                "######",
                "#@$  #",
                "# $$.#",
                "######",
                ]
        maze = Maze(field)
        self.env = pusherenv.PusherEnv(maze)
        self.initial_state = self.env.init()

    def test_init(self):
        pos, boxes = self.initial_state
        self.assertEqual(self.initial_state[0], pos)
        self.assertTrue(self.initial_state[1], boxes)

    def test_get_actions(self):
        actions = self.env.get_actions(self.initial_state)
        self.assertEqual(2, len(actions))
        cmds = [a.get_cmd() for a in actions]
        self.assertTrue(RIGHT in cmds)
        self.assertTrue(DOWN in cmds)

    def test_get_actions_next_two_boxes(self):
        pos, boxes = self.initial_state
        s = ((1,2), boxes)
        actions = self.env.get_actions(s)
        self.assertEqual(1, len(actions))
        self.assertEqual(UP, actions[0].get_cmd())

    def test_predit(self):
        next_s = self.env.predict(self.initial_state, Action(RIGHT))
        next_pos, next_boxes = next_s
        self.assertEqual((2,1), next_pos)
        self.assertEqual(sorted(((3,1), (2,2), (3,2))), sorted(next_boxes))

    def test_estim_cost(self):
        cost = self.env.estim_cost(self.initial_state)
        self.assertEqual(4, cost)

    def test_index_nearest(self):
        targets = ((1,2), (2,8))
        self.assertEquals(0, pusherenv._index_nearest((1,2), targets))
        self.assertEquals(1, pusherenv._index_nearest((1,7), targets))

if __name__ == "__main__":
    unittest.main()

