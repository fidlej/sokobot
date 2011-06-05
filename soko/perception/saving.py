
from libctw import formatting

from soko.perception import perceiving

STORE_FILENAME = "percepts.txt"


def load_training_seqs():
    with open(STORE_FILENAME) as input:
        training_seqs = [line.rstrip("\n\r") for line in
                input.readlines()]

    return training_seqs


def save_perception(env, path):
    bits = _get_seen_bits(env, path)
    with open(STORE_FILENAME, "ab") as output:
        output.write(formatting.to_seq(bits))
        output.write("\n")


def _get_seen_bits(env, path):
    bits = []
    perceiver = perceiving.SokobanPerceiver()
    s = env.init()
    bits += perceiver.encode_state(env, s)
    for a in path:
        bits += perceiver.encode_action(a)
        s = env.predict(s, a)
        bits += perceiver.encode_state(env, s)

    return bits

