import math


class PageInfo:
    def __init__(self, current_page, per_page, total_pages, total_items, has_previous, has_next, data):
        self.currentPage = current_page
        self.perPage = per_page
        self.totalPages = total_pages
        self.totalItems = total_items
        self.hasPrevious = has_previous
        self.hasNext = has_next
        self.data = list(data) if data is not None else []

    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None or type(self) is not type(obj):
            return False
        return (self.currentPage == obj.currentPage and
                self.perPage == obj.perPage and
                self.totalPages == obj.totalPages and
                self.totalItems == obj.totalItems and
                self.hasPrevious == obj.hasPrevious and
                self.hasNext == obj.hasNext and
                self.data == obj.data)

    def __hash__(self):
        result = self.currentPage
        result = 31 * result + self.perPage
        result = 31 * result + self.totalPages
        result = 31 * result + self.totalItems
        result = 31 * result + (1 if self.hasPrevious else 0)
        result = 31 * result + (1 if self.hasNext else 0)
        result = 31 * result + hash(tuple(self.data))
        return result


class SearchResult:
    def __init__(self, keyword, total_results, total_pages, results):
        self.keyword = keyword
        self.totalResults = total_results
        self.totalPages = total_pages
        self.results = list(results) if results is not None else []

    def __eq__(self, obj):
        if self is obj:
            return True
        if obj is None or type(self) is not type(obj):
            return False
        return (self.totalResults == obj.totalResults and
                self.totalPages == obj.totalPages and
                self.keyword == obj.keyword and
                self.results == obj.results)

    def __hash__(self):
        result = hash(self.keyword)
        result = 31 * result + self.totalResults
        result = 31 * result + self.totalPages
        result = 31 * result + hash(tuple(self.results))
        return result


class PageUtil:
    def __init__(self, data, page_size):
        self.data = data
        self.pageSize = page_size
        self.totalItems = len(data)
        self.totalPages = math.ceil(self.totalItems / page_size)

    def getPage(self, page_number):
        if page_number < 1 or page_number > self.totalPages:
            return []
        start_index = (page_number - 1) * self.pageSize
        end_index = min(start_index + self.pageSize, self.totalItems)
        return self.data[start_index:end_index]

    def getPageInfo(self, page_number):
        if page_number < 1 or page_number > self.totalPages:
            return PageInfo(0, self.pageSize, self.totalPages, self.totalItems, False, False, [])
        start_index = (page_number - 1) * self.pageSize
        end_index = min(start_index + self.pageSize, self.totalItems)
        page_data = self.data[start_index:end_index]
        has_previous = page_number > 1
        has_next = page_number < self.totalPages
        return PageInfo(
            page_number,
            self.pageSize,
            self.totalPages,
            self.totalItems,
            has_previous,
            has_next,
            page_data
        )

    def search(self, keyword):
        results = [item for item in self.data if keyword in str(item)]
        num_results = len(results)
        num_pages = math.ceil(num_results / self.pageSize)
        return SearchResult(
            keyword,
            num_results,
            num_pages,
            results
        )