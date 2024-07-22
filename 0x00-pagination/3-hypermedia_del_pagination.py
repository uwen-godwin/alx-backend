from typing import List, Tuple, Dict
import csv

def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Returns a tuple of size two containing a start index and an end index
    corresponding to the range of indexes to return in a list for those
    particular pagination parameters.
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return start_index, end_index

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
            self.__indexed_dataset = {i: dataset[i] for i in range(len(dataset))}
        return self.__indexed_dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Takes two integer arguments page with default value 1 and page_size with default value 10.
        Uses index_range to find the correct indexes to paginate the dataset correctly and return
        the appropriate page of the dataset (i.e., the correct list of rows).
        If the input arguments are out of range for the dataset, an empty list should be returned.
        """
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start_index, end_index = index_range(page, page_size)
        dataset = self.dataset()

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict[str, any]:
        """
        Takes two integer arguments index with default value 0 and page_size with default value 10.
        Returns a dictionary with key-value pairs as described:
        - index: the current start index of the return page. That is the index of the first item in the current page.
        - next_index: the next index to query with.
        - page_size: the current page size.
        - data: the dataset page (the same as get_page).
        """
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
            while next_index in dataset and next_index < total_items:
                next_index += 1
            if next_index >= total_items:
                next_index = None

        return {
            'index': index,
            'next_index': next_index,
            'page_size': page_size,
            'data': data
        }
