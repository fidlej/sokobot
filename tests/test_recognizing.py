
from nose.tools import assert_equal

from soko.struct import recognizing
from soko.mazing import Maze
from test_preproc import parse_field

def test_is_matching():
    shift = (2,1)
    pattern = parse_field("""\
?   ?
 $ .#
   @#
    #
?###?""")

    maze = Maze("""\
#######
#     #
## $ .#
##   @#
#     #
#######""".splitlines())


    assert_equal(True, recognizing._is_matching(shift, pattern, maze))
    assert_equal(False, recognizing._is_matching((0,0), pattern, maze))
    assert_equal(False, recognizing._is_matching((1,2), pattern, maze))


def _parse_field(input):
    lines = input.splitlines()
    return  modeling.immutablize(lines)

