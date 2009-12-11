
import logging

def use_psyco():
    try:
        import psyco
        psyco.full()
    except ImportError:
        logging.debug("psyco is not available")
        pass

def count_recursion(fn):
    def wrapper(*args, **kw):
        wrapper.nesting += 1
        if wrapper.nesting > wrapper.max_nesting:
            wrapper.max_nesting = wrapper.nesting
            if wrapper.max_nesting % 10 == 0:
                logging.debug("max_nesting: %s", wrapper.max_nesting)

        try:
            return fn(*args, **kw)
        finally:
            wrapper.nesting -= 1

    wrapper.nesting = 0
    wrapper.max_nesting = 0
    return wrapper

def suppress_logging(fn):
    def wrapper(*args, **kw):
        logger = logging.getLogger()
        orig_level = logger.level
        logger.setLevel(logging.WARNING)
        try:
            return fn(*args, **kw)
        finally:
            logger.setLevel(orig_level)

    return wrapper

def ensure_high_recursionlimit():
    import sys
    if sys.getrecursionlimit() < 5000:
        sys.setrecursionlimit(5000)

