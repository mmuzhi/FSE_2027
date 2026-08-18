import math
from dataclasses import dataclass
from typing import List, Optional


@dataclass(unsafe_hash=True)
class PageInfo:
    currentPage: int
    perPage: int
    totalPages: int
    totalItems: int
    hasPrevious: bool
    hasNext: bool
    data: Optional[List[int]] = None

    def __post_init__(self):
        self.data = list(self.data) if self.data is not None else []


@dataclass(unsafe_hash=True)
class SearchResult:
    keyword: str
    totalResults: int
    totalPages: int
    results: Optional[List[int]] = None

    def __post_init__(self):
        self.results = list(self.results) if self.results is not None else []


class PageUtil:
    def __init__(self, data: List[int], pageSize: int):
        self.data = data
        self.pageSize = pageSize
        self.totalItems = len(data)
        self.totalPages = self._ceil_div(self.totalItems, pageSize)

    @staticmethod
    def _ceil_div(total_items: int, page_size: int) -> int:
        # Mimics (int) Math.ceil((double) totalItems / pageSize):
        # pageSize == 0 -> +Infinity (-> Integer.MAX_VALUE) when totalItems > 0,
        # NaN (-> 0) when totalItems == 0.
        if page_size == 0:
            return 0 if total_items == 0 else 2147483647
        return math.ceil(total_items / page_size)

    def getPage(self, pageNumber: int) -> List[int]:
        if pageNumber < 1 or pageNumber > self.totalPages:
            return []

        startIndex = (pageNumber - 1) * self.pageSize
        endIndex = min(startIndex + self.pageSize, self.totalItems)
        return self.data[startIndex:endIndex]

    def getPageInfo(self, pageNumber: int) -> PageInfo:
        if pageNumber < 1 or pageNumber > self.totalPages:
            return PageInfo(0, self.pageSize, self.totalPages, self.totalItems,
                            False, False, [])

        startIndex = (pageNumber - 1) * self.pageSize
        endIndex = min(startIndex + self.pageSize, self.totalItems)
        pageData = self.data[startIndex:endIndex]

        hasPrevious = pageNumber > 1
        hasNext = pageNumber < self.totalPages

        return PageInfo(pageNumber, self.pageSize, self.totalPages, self.totalItems,
                        hasPrevious, hasNext, pageData)

    def search(self, keyword: str) -> SearchResult:
        results = [item for item in self.data if keyword in str(item)]

        numResults = len(results)
        numPages = self._ceil_div(numResults, self.pageSize)

        return SearchResult(keyword, numResults, numPages, results)