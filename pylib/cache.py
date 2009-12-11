
def memoize(f):
    """A decorator to memorize the returned results.
    """
    cache = {}
    def wraper(*args):
        if args in cache:
            return cache[args]

        result = f(*args)
        cache[args] = result
        return result

    return wraper

def selfmem(f):
    """A decorator for a method.
    It remembers the results inside the 'self'.
    """
    def wraper(self, *args):
        try:
            cache = self.selfmem
        except AttributeError:
            cache = {}
            self.selfmem = cache

        if args in cache:
            return cache[args]

        result = f(self, *args)
        cache[args] = result
        return result

    return wraper

