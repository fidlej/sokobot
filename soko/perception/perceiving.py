
from soko.env.env import Action
from soko.env import pathfinder, coding

MASK = (
        "  1  ",
        "  1  ",
        "11 11",
        "  1  ",
        "  1  ",
        )

OUTSIDE_MARK = " "


class SokobanPerceiver:
    ACTION_BITS_TO_CMD = {
            (1, 0, 0, 0): pathfinder.UP,
            (0, 1, 0, 0): pathfinder.LEFT,
            (0, 0, 1, 0): pathfinder.RIGHT,
            (0, 0, 0, 1): pathfinder.DOWN
            }

    CMD_TO_ACTION_BITS = dict((v, k) for k, v in
            ACTION_BITS_TO_CMD.iteritems())

    def __init__(self):
        self.num_percept_bits = len(_encode_percept([], 0, 0))

    def get_num_percept_bits(self):
        return self.num_percept_bits

    def get_num_action_bits(self):
        return len(self.CMD_TO_ACTION_BITS[0])

    def encode_action(self, action):
        """Encodes up, left, right, down action bits.
        The order of the directions corresponds to the perception bits.
        """
        return self.CMD_TO_ACTION_BITS[action.get_cmd()]

    def decode_action(self, bits):
        cmd = self.ACTION_BITS_TO_CMD.get(tuple(bits))
        if cmd is None:
            raise ValueError("Invalid action bits: %s" % bits)

        return Action(cmd)

    def encode_state(self, env, s):
        field = env.format(s)
        rows = field.split("\n")
        (player_pos, boxes) = s
        bits = _encode_percept(rows, *player_pos)
        assert len(bits) == self.num_percept_bits
        return bits


def _encode_percept(rows, center_x, center_y):
    mask_w = len(MASK[0])
    mask_h = len(MASK)
    assert mask_w % 2 == 1
    assert mask_h % 2 == 1
    tiles = _get_masked(rows, center_x - mask_w//2, center_y - mask_h//2)
    bits = []
    bits += _mark_presence(tiles, coding.BOX_MARKS)
    bits += _mark_presence(tiles, coding.WALL_MARKS)
    bits += _mark_presence(tiles, coding.TARGET_MARKS)
    return bits


def _get_masked(rows, corner_x, corner_y):
    tiles = []
    for mask_y, mask_row in enumerate(MASK):
        y = corner_y + mask_y
        for mask_x, flag in enumerate(mask_row):
            if flag != "1":
                continue

            x = corner_x + mask_x
            if x < 0 or y < 0:
                tile = OUTSIDE_MARK
            else:
                try:
                    tile = rows[y][x]
                except IndexError:
                    tile = OUTSIDE_MARK

            tiles.append(tile)

    return tiles


def _mark_presence(tiles, marks):
    bits = [0] * len(tiles)
    for i, tile in enumerate(tiles):
        bits[i] = _bit(tile in marks)

    return bits


def _bit(boolean):
    return 1 if boolean else 0

