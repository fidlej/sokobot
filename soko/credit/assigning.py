
MARGIN = 1

def reward(actions, states):
    #TODO: ignore non-struct states and actions
    for s, a in zip(states, actions):
        move_id = _identify_move(s, a)
        print "============"
        for row in move_id:
            print "".join(row)

def punish(actions, states):
    pass


def _identify_move(s, a):
    pattern = []
    effects = a.get_cmd()
    xs = [pos[0] for pos, mark in effects]
    ys = [pos[1] for pos, mark in effects]
    for y in xrange(min(ys) - MARGIN, max(ys) + MARGIN + 1):
        row = s[y]
        pattern_row = []
        pattern.append(pattern_row)
        for x in xrange(min(xs) - MARGIN, max(xs) + MARGIN + 1):
            pattern_row.append(row[x])

    return pattern
