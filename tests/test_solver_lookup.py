
import unittest

from soko.solver import solver_lookup
from soko.env.relaxedenv import RelaxedEnv

class Test(unittest.TestCase):
    def setUp(self):
        self.level_filename = "data/sokoban/level001.txt"

    def test_extract_prefixes(self):
        name, wrappers = solver_lookup._extract_prefixes("relaxrelaxedrelaxida")
        self.assertEquals("ida", name)
        self.assertEquals([RelaxedEnv, RelaxedEnv, RelaxedEnv], wrappers)

