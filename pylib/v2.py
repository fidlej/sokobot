
def sum(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (x1 + x2, y1 + y2)

def diff(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (x1 - x2, y1 - y2)

def scale(shift, amount):
    x, y = shift
    return (x * amount, y * amount)
