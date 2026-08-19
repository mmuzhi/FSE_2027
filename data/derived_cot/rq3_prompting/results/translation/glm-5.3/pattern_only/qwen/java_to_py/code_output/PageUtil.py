import math
from typing import List, Optional


class PageUtil:
    def __init__(self, data: List[int], pageSize: int):
        self.data = data
        self.pageSize = pageSize
        self.totalItems = len(data)
        self.totalPages = self._ceilDivAsInt(self.totalItems, pageSize)

    @staticmethod
    def _ceilDivAsInt(count: int, pageSize: int) -> int:
        # Mimics Java: (int) Math.ceil((double) count / pageSize)
        # Java double division by zero yields Infinity/NaN (no exception);
        # the int cast saturates Infinity to Integer.MAX_VALUE and NaN to 0.
        if pageSize == 0:
            return 2147483647 if count > 0 else 0
        return math.ceil(count / pageSize)

    def getPage(self, pageNumber: int) -> List[int]:
        if pageNumber < 1 or pageNumber > self.totalPages:
            return []
        startIndex = (pageNumber - 1) * self.pageSize
        endIndex = min(startIndex + self.pageSize, self.totalItems)
        return self.data[startIndex:endIndex]

    def getPageInfo(self, pageNumber: int) -> "PageUtil.PageInfo":
        if pageNumber < 1 or pageNumber > self.totalPages:
            return PageUtil.PageInfo(0, self.pageSize, self.totalPages,
                                     self.totalItems, False, False, [])
        startIndex = (pageNumber - 1) * self.pageSize
        endIndex = min(startIndex + self.pageSize, self.totalItems)
        pageData = self.data[startIndex:endIndex]
        hasPrevious = pageNumber > 1
        hasNext = pageNumber < self.totalPages
        return PageUtil.PageInfo(pageNumber, self.pageSize, self.totalPages,
                                 self.totalItems, hasPrevious, hasNext, pageData)

    def search(self, keyword: str) -> "PageUtil.SearchResult":
        results = [item for item in self.data if keyword in str(item)]
        numResults = len(results)
        numPages = self._ceilDivAsInt(numResults, self.pageSize)
        return PageUtil.SearchResult(keyword, numResults, numPages, results)

    class PageInfo:
        def __init__(self, currentPage: int, perPage: int, totalPages: int,
                     totalItems: int, hasPrevious: bool, hasNext: bool,
                     data: Optional[List[int]]):
            self.currentPage = currentPage
            self.perPage = perPage
            self.totalPages = totalPages
            self.totalItems = totalItems
            self.hasPrevious = hasPrevious
            self.hasNext = hasNext
            self.data = list(data) if data is not None else []

        def __eq__(self, obj):
            if self is obj:
                return True
            if obj is None or self.__class__ is not obj.__class__:
                return False
            return (self.currentPage == obj.currentPage and
                    self.perPage == obj.perPage and
                    self.totalPages == obj.totalPages and
                    self.totalItems == obj.totalItems and
                    self.hasPrevious == obj.hasPrevious and
                    self.hasNext == obj.hasNext and
                    self.data == obj.data)

        def __hash__(self):
            return hash((self.currentPage, self.perPage, self.totalPages,
                         self.totalItems, self.hasPrevious, self.hasNext,
                         tuple(self.data)))

    class SearchResult:
        def __init__(self, keyword: str, totalResults: int, totalPages: int,
                     results: Optional[List[int]]):
            self.keyword = keyword
            self.totalResults = totalResults
            self.totalPages = totalPages
            self.results = list(results) if results is not None else []

        def __eq__(self, obj):
            if self is obj:
                return True
            if obj is None or self.__class__ is not obj.__class__:
                return False
            return (self.totalResults == obj.totalResults and
                    self.totalPages == obj.totalPages and
                    self.keyword == obj.keyword and
                    self.results == obj.results)

        def __hash__(self):
            return hash((self.keyword, self.totalResults, self.totalPages,
                         tuple(self.results)))