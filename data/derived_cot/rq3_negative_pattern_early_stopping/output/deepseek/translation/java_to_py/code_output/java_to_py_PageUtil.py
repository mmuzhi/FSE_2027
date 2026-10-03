from math import ceil
from typing import List, Optional

class PageUtil:
    def __init__(self, data: List[int], page_size: int):
        self._data = data
        self._page_size = page_size
        self._total_items = len(data)
        self._total_pages = max(0, (self._total_items + page_size - 1) // page_size) if page_size > 0 else 0

    def get_page(self, page_number: int) -> List[int]:
        if page_number < 1 or page_number > self._total_pages:
            return []
        start = (page_number - 1) * self._page_size
        end = min(start + self._page_size, self._total_items)
        return self._data[start:end]

    def get_page_info(self, page_number: int) -> 'PageInfo':
        if page_number < 1 or page_number > self._total_pages:
            return PageInfo(0, self._page_size, self._total_pages, self._total_items, False, False, [])
        start = (page_number - 1) * self._page_size
        end = min(start + self._page_size, self._total_items)
        page_data = self._data[start:end]
        has_previous = page_number > 1
        has_next = page_number < self._total_pages
        return PageInfo(page_number, self._page_size, self._total_pages, self._total_items, has_previous, has_next, page_data)

    def search(self, keyword: str) -> 'SearchResult':
        results = [item for item in self._data if keyword in str(item)]
        num_results = len(results)
        num_pages = max(0, (num_results + self._page_size - 1) // self._page_size) if self._page_size > 0 else 0
        return SearchResult(keyword, num_results, num_pages, results)


class PageInfo:
    def __init__(self, current_page: int, per_page: int, total_pages: int, total_items: int,
                 has_previous: bool, has_next: bool, data: Optional[List[int]] = None):
        self.current_page = current_page
        self.per_page = per_page
        self.total_pages = total_pages
        self.total_items = total_items
        self.has_previous = has_previous
        self.has_next = has_next
        self.data = list(data) if data is not None else []

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, PageInfo):
            return False
        return (self.current_page == other.current_page and
                self.per_page == other.per_page and
                self.total_pages == other.total_pages and
                self.total_items == other.total_items and
                self.has_previous == other.has_previous and
                self.has_next == other.has_next and
                self.data == other.data)

    def __hash__(self) -> int:
        result = self.current_page
        result = 31 * result + self.per_page
        result = 31 * result + self.total_pages
        result = 31 * result + self.total_items
        result = 31 * result + (1 if self.has_previous else 0)
        result = 31 * result + (1 if self.has_next else 0)
        result = 31 * result + hash(tuple(self.data))
        return result

    def __repr__(self) -> str:
        return (f"PageInfo(current_page={self.current_page}, per_page={self.per_page}, "
                f"total_pages={self.total_pages}, total_items={self.total_items}, "
                f"has_previous={self.has_previous}, has_next={self.has_next}, data={self.data})")


class SearchResult:
    def __init__(self, keyword: str, total_results: int, total_pages: int, results: Optional[List[int]] = None):
        self.keyword = keyword
        self.total_results = total_results
        self.total_pages = total_pages
        self.results = list(results) if results is not None else []

    def __eq__(self, other: object) -> bool:
        if self is other:
            return True
        if not isinstance(other, SearchResult):
            return False
        return (self.keyword == other.keyword and
                self.total_results == other.total_results and
                self.total_pages == other.total_pages and
                self.results == other.results)

    def __hash__(self) -> int:
        result = hash(self.keyword)
        result = 31 * result + self.total_results
        result = 31 * result + self.total_pages
        result = 31 * result + hash(tuple(self.results))
        return result

    def __repr__(self) -> str:
        return (f"SearchResult(keyword={self.keyword!r}, total_results={self.total_results}, "
                f"total_pages={self.total_pages}, results={self.results})")