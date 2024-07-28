#!/usr/bin/env python3
"""
Module for simple pagination of a dataset from Popular_Baby_Names.csv.
"""

from typing import List, Tuple
import csv


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple containing start and end indexes for pagination.

    Args:
        page (int): Page number (starting from 1).
        page_size (int): Number of items per page.

    Returns:
        Tuple[int, int]: Start and end indexes for slicing.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index


class Server:
    """Server class to paginate a dataset of popular baby names."""

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Returns the dataset from the CSV file,
        caching it if not already loaded.

        Returns:
            List[List]: Dataset read from CSV file, excluding header.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                self.__dataset = list(reader)[1:]  # Skip header row
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a specific page of data from the dataset.

        Args:
            page (int, optional): Page number (default is 1).
            page_size (int, optional): Number
            of items per page (default is 10).

        Returns:
            List[List]: Subset of dataset corresponding to the requested page.

        Raises:
            AssertionError: If page or page_size
            are not integers greater than 0.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
