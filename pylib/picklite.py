#!/usr/bin/env python
"""
A simple key-value store based on Pickle and sqlite.

Inspired by Raymond Hettinger's recipe:
http://code.activestate.com/recipes/576638-draft-for-an-sqlite3-based-dbm/

Licensed under MIT License.
Copyright (c) 2010 Ivo Danihelka
Copyright (c) 2009 Raymond Hettinger
"""

__all__ = ['open']

import sqlite3
import UserDict
import cPickle as pickle

sqlite3.register_converter('pickle', pickle.loads)

def _serialize(value):
    return sqlite3.Binary(pickle.dumps(value, protocol=2))

class SQLhash(UserDict.DictMixin):

    def __init__(self, filename=':memory:'):
        MAKE_SHELF = """CREATE TABLE IF NOT EXISTS shelf (
            key TEXT NOT NULL PRIMARY KEY,
            value PICKLE NOT NULL)
            """
        # The detection of types is needed for automatic unpickling.
        self.conn = sqlite3.connect(filename,
                isolation_level=None,
                detect_types=sqlite3.PARSE_DECLTYPES)
        self.conn.execute(MAKE_SHELF)

    def __len__(self):
        GET_LEN =  'SELECT COUNT(*) FROM shelf'
        return self.conn.execute(GET_LEN).fetchone()[0]

    def iterkeys(self):
        return SQLhashKeysView(self)

    def itervalues(self):
        return SQLhashValuesView(self)

    def iteritems(self):
        return SQLhashItemsView(self)

    def keys(self):
        return list(self.iterkeys())

    def values(self):
        return list(self.itervalues())

    def items(self):
        return list(self.iteritems())

    def __iter__(self):
        return iter(self.iterkeys())

    def __contains__(self, key):
        GET_ITEM = 'SELECT value FROM shelf WHERE key = ?'
        return self.conn.execute(GET_ITEM, (key,)).fetchone() is not None

    def __getitem__(self, key):
        GET_ITEM = 'SELECT value FROM shelf WHERE key = ?'
        item = self.conn.execute(GET_ITEM, (key,)).fetchone()
        if item is None:
            raise KeyError(key)
        return item[0]

    def __setitem__(self, key, value):
        ADD_ITEM = 'REPLACE INTO shelf (key, value) VALUES (?,?)'
        value = _serialize(value)
        self.conn.execute(ADD_ITEM, (key, value))

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        DEL_ITEM = 'DELETE FROM shelf WHERE key = ?'
        self.conn.execute(DEL_ITEM, (key,))

    def update(self, items=(), **kwds):
        if hasattr(items, 'items'):
            items = items.items()
        items = ((k, _serialize(v)) for k, v in items)
        UPDATE_ITEMS = 'REPLACE INTO shelf (key, value) VALUES (?, ?)'
        self.conn.executemany(UPDATE_ITEMS, items)
        if kwds:
            self.update(kwds)

    def clear(self):
        CLEAR_ALL = 'DELETE FROM shelf;  VACUUM;'
        self.conn.executescript(CLEAR_ALL)

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __del__(self):
        self.close()

class ListRepr(object):
    def __init__(self, mapping):
        self._mapping = mapping

    def __repr__(self):
        return repr(list(self))

class SQLhashKeysView(ListRepr):

    def __iter__(self):
        GET_KEYS = 'SELECT key FROM shelf ORDER BY ROWID'
        return (row[0] for row in self._mapping.conn.cursor().execute(GET_KEYS))

class SQLhashValuesView(ListRepr):

    def __iter__(self):
        GET_VALUES = 'SELECT value FROM shelf ORDER BY ROWID'
        return (row[0] for row in self._mapping.conn.cursor().execute(GET_VALUES))

class SQLhashItemsView(ListRepr):

    def __iter__(self):
        GET_ITEMS = 'SELECT key, value FROM shelf ORDER BY ROWID'
        return iter(self._mapping.conn.cursor().execute(GET_ITEMS))

def open(file=None):
    if file is not None:
        return SQLhash(file)
    return SQLhash()


if __name__ in '__main___':
    d = SQLhash('example')
    print list(d), 'start'
    d['abc'] = 'lmno'
    print(d['abc'])
    d['abc'] = 'rsvp'
    d['xyz'] = 'pdq'
    print(d.items())
    print(d.values())
    print(d.keys())
    print list(d), 'list'
    d.update(p='x', q='y', r='z')
    print(d.items())

    del d['abc']
    try:
        print(d['abc'])
    except KeyError:
        pass
    else:
        raise Exception('oh noooo!')

    try:
        del d['abc']
    except KeyError:
        pass
    else:
        raise Exception('drat!')

    print(list(d))
    d.clear()
    print(list(d))
    d.update(p='x', q='y', r='z')
    print(list(d))
    d['xyz'] = 'pdq'

    d['pickled'] = {'key':'value', 'other':1234, 'a list':[1,2,'good']}
    print d

    print
    d.close()
