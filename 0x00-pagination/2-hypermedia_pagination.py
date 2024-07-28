#!/usr/bin/env python3
"""
This module provides pagination functionalities for a
dataset of popular baby names.
It includes methods to retrieve paginated data
and hypermedia pagination information.
"""

from typing import List, Tuple, Dict, Any
import csv
import math


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for those
    particular pagination parameters.

    Args:
        page (int): The current page number.
        page_size (int): The number of items per page.

    Returns:
        Tuple[int, int]: The start and end index for
        the given pagination parameters.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names."""
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """Initialize the server with a dataset cache."""
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Returns the cached dataset.

        If the dataset is not cached, it reads from the CSV file and caches it.

        Returns:
            List[List]: The dataset of popular baby names.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Returns a page of the dataset.

        Args:
            page (int): The current page number (default is 1).
            page_size (int): The number of items per page (default is 10).

        Returns:
            List[List]: A list of rows for the specified page.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """
        Returns hypermedia pagination information.

        Args:
            page (int): The current page number (default is 1).
            page_size (int): The number of items per page (default is 10).

        Returns:
            Dict[str, Any]: A dictionary with pagination information.
        """
        data = self.get_page(page, page_size)
        total_items = len(self.dataset())
        total_pages = math.ceil(total_items / page_size)

        hypermedia = {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if page < total_pages else None,
            'prev_page': page - 1 if page > 1 else None,
            'total_pages': total_pages
        }

        return hypermedia
