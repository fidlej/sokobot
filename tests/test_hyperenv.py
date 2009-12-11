
import unittest
import logging

from soko import mazing
from soko.env import hyperenv
from soko.env.pusherenv import PusherEnv, SokobanEnv

class Test(unittest.TestCase):
    def setUp(self):
        field = [
                "#########",
                "#x..o...#",
                "###....G#",
                "#########",
                ]
        maze = mazing.Maze(field)
        self._init_env(maze)
        self.gator = hyperenv.CycleGator()

    def _init_env(self, maze, env_factory=PusherEnv):
        self.env = env_factory(maze)
        self.initial_state = self.env.init()
        return self.initial_state

    def test_pop_nearest(self):
        states = ["hello", "good", "bla"]
        gs = [2, 1, 3]
        opened = {}
        for g, s in zip(gs, states):
            opened[s] = hyperenv.Node(g, s)

        orig_len = len(opened)
        nearest = self.gator._pop_nearest(opened)

        self.assertEqual(orig_len - 1, len(opened))
        self.assertEqual((1, "good"), nearest)

    def test_get_connected(self):
        field = [
                "#######",
                "#x.o..#",
                "###..G#",
                "#######",
                ]
        self._init_env(mazing.Maze(field))

        connected = self.gator.get_connected(self.env, self.initial_state)
        self.assertTrue(self.initial_state in connected)
        self.assertEqual(2, len(connected))

        pos, boxes = self.initial_state
        self.assertTrue(((2,1), boxes) in connected)

    def test_get_connected(self):
        pos, boxes = self.initial_state
        s = (pos, ((4,1),))
        connected = self.gator.get_connected(self.env, s)
        self.assertTrue(s in connected)
        self.assertEqual(11, len(connected))

        self.gator = hyperenv.CycleGator(6)
        connected = self.gator.get_connected(self.env, s)
        self.assertTrue(s in connected)
        self.assertEqual(33, len(connected))

    def test_get_complex_connected(self):
        self._assert_connected("data/pusher/pusher2.txt", PusherEnv)
        for i in range(1, 4):
            self._assert_connected("data/sokoban/sokoban%s.txt" % i, SokobanEnv)

    def _assert_connected(self, maze_filename, env_factory):
        print "Testing:", maze_filename
        maze = mazing.parse_maze(maze_filename)
        s = self._init_env(maze, env_factory)

        self.gator = hyperenv.CycleGator()
        connected = self.gator.get_connected(self.env, s)
        print "num connected:", len(connected)
        self.assertTrue(s in connected)

        for new_s in connected:
            new_connected = self.gator.get_connected(self.env, new_s)
            self.assertEqual(connected, new_connected)


if __name__ == "__main__":
    unittest.main()

