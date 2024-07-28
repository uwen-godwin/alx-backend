#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None,
                        page_size: int = 10) -> Dict[str, Any]:
        """
        Returns a dictionary with pagination details
        that is resilient to deletions.

        Args:
            index (int, optional): The current start index of the return page.
            page_size (int, optional): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary with pagination details.
        """
        if index is None:
            index = 0

        assert isinstance(index, int) and index >= 0
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

        next_index = current_index if current_index < total_items else None

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': data
        }
