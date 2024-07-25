#!/usr/bin/env python3
""" MRU caching """

from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines a MRU caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.usage_order = []

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return

        if key in self.cache_data:
            self.usage_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            last_key = self.usage_order.pop()
            print("DISCARD:", last_key)
            del self.cache_data[last_key]

        self.cache_data[key] = item
        self.usage_order.append(key)

    def get(self, key):
        """ Get an item by key """
        if key is None or key not in self.cache_data:
            return None

        self.usage_order.remove(key)
        self.usage_order.append(key)
        return self.cache_data[key]
