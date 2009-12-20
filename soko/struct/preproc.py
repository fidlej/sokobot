
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
                    queue.append(child)

    return end_states, used_cells

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

