
from nose.tools import assert_equal

from soko.struct.rules.sokorule import PushRule
from soko.struct import modeling, preproc

def test_get_children():
    rules = [PushRule()]
    s = modeling.immutablize("""\
#   #
 $ .#
   @#
    #
#####""".splitlines())

    end_states, used_cells = preproc.detect_end_states(s, rules)
    assert_equal(6, len(end_states))

