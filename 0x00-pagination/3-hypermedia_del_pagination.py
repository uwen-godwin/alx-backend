#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset."""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]
        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0."""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {i:dataset[i] for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """Provide pagination that is resilient to row deletions."""
        assert isinstance(index, int) and index >= 0
        assert isinstance(page_size, int) and page_size > 0
        
        dataset = self.indexed_dataset()
        total_items = len(dataset)
        
        if index >= total_items:
            raise AssertionError("Index out of range")

        data = []
        current_index = index
        next_index = index

        while len(data) < page_size and next_index < total_items:
            item = dataset.get(next_index, None)
            if item:
                data.append(item)
                current_index = next_index
            next_index += 1

        next_index = current_index + 1

        while next_index < total_items and next_index not in dataset:
            next_index += 1

        if next_index >= total_items:
            next_index = None

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': data#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0,
                        page_size: int = 10) -> Dict[str, Any]:
        """Returns a dictionary with pagination details"""
        # Validate index
        if index is None or not isinstance(index, int) or index < 0:
            raise AssertionError("Index must be a non-negative integer")

        assert isinstance(page_size, int) and page_size > 0

        dataset = self.indexed_dataset()
        total_items = len(dataset)

        if index >= total_items:
            raise AssertionError("Index out of range")

        data = []
        current_index = index

        # Adjust the index to skip deleted items
        while len(data) < page_size and current_index < total_items:
            if current_index in dataset:
                data.append(dataset[current_index])
            current_index += 1

        next_index = index + page_size
        if next_index >= total_items:
            next_index = None
        else:
            # Adjust next_index to avoid pointing to a deleted item
            while next_index not in dataset and next_index < total_items:
                next_index += 1
            if next_index >= total_items:
                next_index = None

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': data
        }
        }
