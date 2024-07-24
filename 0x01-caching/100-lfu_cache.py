#!/usr/bin/env python3
""" LFU caching """

from base_caching import BaseCaching
from collections import defaultdict


class LFUCache(BaseCaching):
    """ LFUCache defines a LFU caching system """

    def __init__(self):
        """ Initialize """
        super().__init__()
        self.cache_data = {}
        self.usage_freq = defaultdict(int)
        self.min_freq = None

    def put(self, key, item):
        """ Add an item in the cache """
        if key is None or item is None:
            return
        if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            if self.min_freq is not None:
                min_freq_keys = [k for k, v in
                                 self.usage_freq.items() if v == self.min_freq]
                lfu_key = min_freq_keys[0]
                print("DISCARD:", lfu_key)
                self.cache_data.pop(lfu_key)
                self.usage_freq.pop(lfu_key)
        self.cache_data[key] = item
        self.usage_freq[key] += 1
        self.min_freq = min(self.usage_freq.values())

    def get(self, key):
        """ Get an item by key """
        if key in self.cache_data:
            self.usage_freq[key] += 1
            self.min_freq = min(self.usage_freq.values())
            return self.cache_data.get(key, None)
        return None
