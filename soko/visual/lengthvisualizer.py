
class LengthVisualizer(object):
    def __init__(self, call_counter):
        self.call_counter = call_counter

    def render(self, env, path):
        num_visited = self.call_counter.get_count()

        total_cost = calc_path_cost(path)
        output = ""
        output += "num_visited: %s\n" % num_visited
        output += "length: %s\n" % len(path)
        output += "cost: %s\n" % (total_cost,)
        return output

def calc_path_cost(path):
    """Calculates cost of the given path
    by revisiting its states.
    """
    costs = calc_costs(path)
    return sum(costs)

def calc_costs(path):
    """Returns the cost of the path steps.
    """
    return [a.get_cost() for a in path]

