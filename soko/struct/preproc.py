
from soko.env.coding import UNKNOWN_MARK
from soko.struct import modeling

def detect_end_states(pattern, rules):
    """Returns a (end_states, used_cells) pair
    with the end states for the pattern
    and the informative cell positions of the pattern.
    """
    end_states = []
    used_cells = set()
    seen = set([pattern])
    queue = [pattern]
    while queue:
        s = queue.pop(-1)
        children = _get_children(rules, s, used_cells)
        if children is None:
            end_states.append(s)
        else:
            for child in children:
                if child not in seen:
                    seen.add(child)
                    if _is_goaling(rules, s, child):
                        end_states.append(child)
                    else:
                        queue.append(child)

    return end_states, used_cells

def generalize(pattern, used_cells):
    """Erases the unsed positions.
    """
    new_pattern = modeling.mutablize(pattern)
    for y, row in enumerate(pattern):
        for x in xrange(len(row)):
            pos = (x, y)
            if pos not in used_cells:
                new_pattern[y][x] = UNKNOWN_MARK

    return modeling.immutablize(new_pattern)

def _get_children(rules, s, used_cells):
    """Returns a list of children or None
    when the given state is an end state of its pattern.
    An end state does not have enough info for a rule.
    """
    local_used_cells = set()
    children = []
    for rule in rules:
        rule_children = rule.get_children(s, local_used_cells)
        if rule_children is None:
            return None
        else:
            children += rule_children

    used_cells.update(local_used_cells)
    return children

def _is_goaling(rules, s, child):
    """Returns true if the transition leads
    to a possible part of a global goal state.
    """
    for rule in rules:
        if rule.is_goaling(s, child):
            return True

    return False

