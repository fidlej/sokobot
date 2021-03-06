
from nose.tools import assert_equal

from soko.struct.rules.sokorule import PushRule, SokobanGoalRule
from soko.struct import modeling

def test_get_children():
    rule = PushRule()
    s = (
            "#   #",
            "#@. #",
            " $  #",
            "    #",
            "#####",
            )

    used_cells = set()
    children = rule.get_children(s, used_cells)
    assert_equal(3, len(children))
    _assert_contains(children,
            ("#   #",
            "# + #",
            " $  #",
            "    #",
            "#####",
            ))
    _assert_contains(children,
            ("#@  #",
            "# . #",
            " $  #",
            "    #",
            "#####",
            ))
    _assert_contains(children,
            ("#   #",
            "# . #",
            " @  #",
            " $  #",
            "#####",
            ))

    used_s = modeling.mutablize(s)
    for pos in used_cells:
        x, y = pos
        used_s[y][x] = "!"

    assert_equal(modeling.immutablize(
        (
            "#!  #",
            "!!! #",
            " !  #",
            " !  #",
            "#####",
        )), modeling.immutablize(used_s))

def test_get_children_from_end_state():
    s = modeling.immutablize("""\
#$  #
 @ .#
    #
    #
#####""".splitlines())
    rule = PushRule()
    used_cells = set()
    children = rule.get_children(s, used_cells)
    assert_equal(None, children)
    assert_equal(set(), used_cells)

def test_is_goaling():
    rule = SokobanGoalRule()
    s = (
            "#   #",
            "#  .#",
            "   $#",
            "   @#",
            "#####",
            )
    next_s = (
            "#   #",
            "#  *#",
            "   @#",
            "    #",
            "#####",
            )
    assert_equal(True, rule.is_goaling(s, next_s))
    assert_equal(False, rule.is_goaling(next_s, s))
    assert_equal(False, rule.is_goaling(next_s, next_s))

def _assert_contains(childern, s):
    s = modeling.immutablize(s)
    assert s in childern
