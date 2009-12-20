
from nose.tools import assert_equal

from soko.struct.rules.sokorule import PushRule
from soko.struct import modeling, preproc

def test_get_children():
    rules = [PushRule()]
    s = _parse_field("""\
#   #
 $ .#
   @#
    #
#####""")

    end_states, used_cells = preproc.detect_end_states(s, rules)
    assert_equal(6, len(end_states))

    assert_equal(_parse_field("""\
%   %
 $ .#
   @#
    #
%###%"""), preproc.generalize(s, used_cells))


def _parse_field(input):
    lines = input.splitlines()
    return  modeling.immutablize(lines)

