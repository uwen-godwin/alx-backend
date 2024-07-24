#!/usr/bin/env python3
""" LIFO caching """

from base_caching import BaseCaching

class LIFOCache(BaseCaching):
    """ LIFOCache defines a LIFO caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # Find the last key in the dictionary
            last_key = next(reversed(self.cache_data))
            # Print the discarded key
            print("DISCARD:", last_key)
            # Remove the last item
            self.cache_data.pop(last_key)
        # Add the new item to the cache
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key """
        return self.cache_data.get(key, None)
