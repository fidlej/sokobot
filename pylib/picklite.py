#!/usr/bin/env python
"""
A simple key-value store based on Pickle and sqlite.

Inspired by Raymond Hettinger's recipe:
http://code.activestate.com/recipes/576638-draft-for-an-sqlite3-based-dbm/
"""

__all__ = ['open']

import sqlite3
import UserDict
import cPickle as pickle

#sqlite3.register_converter('pickle', pickle.loads)

class SQLhash(UserDict.DictMixin):

    def __init__(self, filename=':memory:'):
        MAKE_SHELF = """CREATE TABLE IF NOT EXISTS shelf (
            key TEXT NOT NULL PRIMARY KEY,
            value PICKLE NOT NULL)
            """
        self.conn = sqlite3.connect(filename)
        self.conn.execute(MAKE_SHELF)
        self.conn.commit()

    def __len__(self):
        GET_LEN =  'SELECT COUNT(*) FROM shelf'
        return self.conn.execute(GET_LEN).fetchone()[0]

    def keys(self):
        return SQLhashKeysView(self)

    def values(self):
        return SQLhashValuesView(self)

    def items(self):
        return SQLhashItemsView(self)

    def __iter__(self):
        return iter(self.keys())

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
        self.conn.execute(ADD_ITEM, (key, value))
        self.conn.commit()

    def __delitem__(self, key):
        if key not in self:
            raise KeyError(key)
        DEL_ITEM = 'DELETE FROM shelf WHERE key = ?'
        self.conn.execute(DEL_ITEM, (key,))
        self.conn.commit()

    def update(self, items=(), **kwds):
        if hasattr(items, 'items'):
            items = items.items()
        UPDATE_ITEMS = 'REPLACE INTO shelf (key, value) VALUES (?, ?)'
        self.conn.executemany(UPDATE_ITEMS, items)
        self.conn.commit()
        if kwds:
            self.update(kwds)

    def clear(self):
        CLEAR_ALL = 'DELETE FROM shelf;  VACUUM;'
        self.conn.executescript(CLEAR_ALL)
        self.conn.commit()

    def close(self):
        if self.conn is not None:
            self.conn.commit()
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
    for d in SQLhash(), SQLhash('example'):
        print(list(d), 'start')
        d['abc'] = 'lmno'
        print(d['abc'])
        d['abc'] = 'rsvp'
        d['xyz'] = 'pdq'
        print(d.items())
        print(d.values())
        print(d.keys())
        print(list(d), 'list')
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

        print()
        d.close()
