
from nose.tools import assert_equal

from soko.struct.rules.sokorule import PushRule
from soko.struct import modeling

def test_get_children():
    rule = PushRule()
    s = (
            "#   #",
            " @ .#",
            " $  #",
            "    #",
            "#####",
            )

    used_cells = set()
    children = rule.get_children(s, used_cells)
    assert_equal(4, len(children))
    _assert_contains(children,
            ("#   #",
            "  @.#",
            " $  #",
            "    #",
            "#####",
            ))
    _assert_contains(children,
            ("#   #",
            "@  .#",
            " $  #",
            "    #",
            "#####",
            ))
    _assert_contains(children,
            ("#@  #",
            "   .#",
            " $  #",
            "    #",
            "#####",
            ))
    _assert_contains(children,
            ("#   #",
            "   .#",
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
            "!!!.#",
            " !  #",
            " !  #",
            "#####",
        )), modeling.immutablize(used_s))

def _assert_contains(childern, s):
    s = modeling.immutablize(s)
    assert s in childern
