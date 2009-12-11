
def number(value):
    if value is None:
        return value

    ornated = []
    separator = ","
    for i, c in enumerate(reversed(str(value))):
        if i > 0 and i % 3 == 0:
            ornated.insert(0, separator)
        ornated.insert(0, c)
    return ''.join(ornated)

