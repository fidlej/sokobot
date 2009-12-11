
import unittest

from soko.stats.tasking import Task
from soko.stats import resulting

class Test(unittest.TestCase):
    def setUp(self):
        self.level_filename = "data/sokoban/level001.txt"

    def test_get_solution_filename(self):
        self.assert_suffix("ida", "ida")
        self.assert_suffix("relaxida", "relaxida")
        self.assert_suffix("relaxida,estim_limit=True", "relaxida,estim_limit=True")
        self.assert_suffix("ida,var=(1,-2,3)", "ida,var=(1,-2,3)")
        self.assert_suffix("ida,var=_good_", "ida,var='good'")

    def assert_suffix(self, suffix, spec):
        task = Task(self.level_filename, spec)
        expected = "../export/solutions/%s_%s" % (self.level_filename, suffix)
        self.assertEquals(expected, resulting._get_solution_filename(task))

