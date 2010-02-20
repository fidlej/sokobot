
import cPickle as pickle
from pylib import disk

class Storage(object):
    def __init__(self, filename):
        self.filename = filename

    def load(self, default=None):
        try:
            input = open(self.filename, "rb")
        except IOError:
            return default

        value = pickle.load(input)
        input.close()
        return value

    def save(self, value):
        disk.store_content(self.filename, pickle.dumps(value))

