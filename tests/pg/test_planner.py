
import logging
import unittest

from soko import mazing
from soko.estim.pg import extender_pusher, estimator
from soko.env.pusherenv import SokobanEnv

class Test(unittest.TestCase):
    def setUp(self):
        level_filename = "data/sokoban/microban/level001.txt"
        self.env = SokobanEnv(mazing.parse_maze(level_filename))
        self.extender = extender_pusher.SokobanExtender(self.env)

    def test_plan_graph(self):
        s = self.env.init()
        planner = estimator.GraphPlanner(self.extender)

        graph, goal = planner.plan_graph(s)
        self.assertTrue(goal is not None)
        self.assertEquals(7, len(graph.layers))

        new_values = graph.reach.get_new_values()
        self.assertEquals(3, len(new_values))
        self.assertEquals(sorted([('o1', (2,1)), ('o1', (1,2)), ('o1', (4,3))]), sorted(new_values))

        plan = estimator._extract_plan(graph, goal)
        self._check_plan(s, plan)

    def _check_plan(self, s, level_actions):
        effects = self.extender.reset(s)
        logging.debug("effects: %s", effects)
        reach = estimator.Reach()
        reach.extend_reach(effects)
        reachable = reach.get_reachable()

        self.assertEquals(9, estimator._calc_seq_cost(level_actions))

        for actions in level_actions:
            for action in actions:
                effects = action.get_effects()
                logging.debug("effects: %s", effects)
                pres = action.get_pres()
                for value, var in pres:
                    self.assertTrue(reachable.is_in(value, var))

                reach.extend_reach(effects)


