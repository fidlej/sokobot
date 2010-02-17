
from nose.tools import assert_equal

from soko.struct.rules.sokorule import PushRule, SOKOBAN_RULES
from soko.struct import modeling, preproc

def test_get_children():
    rules = [PushRule()]
    s = parse_field("""\
#   #
 $ .#
   @#
    #
#####""")

    end_states, used_cells, num_seen = preproc.detect_end_states(s, rules)
    assert_equal(6, len(end_states))
    assert_equal(14, num_seen)
    end_states.sort()
    assert_equal(parse_field("""\
#   #
 $ .#
    #
@   #
#####"""), end_states[0])

    assert_equal(parse_field("""\
?   ?
 $ .#
   @#
    #
?###?"""), preproc.generalize(s, used_cells))

def test_num_seen():
    rules = SOKOBAN_RULES
    s = parse_field("""\
## ##
#    
#@ # 
#  # 
#####""")

    end_states, used_cells, num_seen = preproc.detect_end_states(s, rules)
    assert_equal(2, len(end_states))
    assert_equal(9, num_seen)

def parse_field(input):
    lines = input.splitlines()
    return  modeling.immutablize(lines)

