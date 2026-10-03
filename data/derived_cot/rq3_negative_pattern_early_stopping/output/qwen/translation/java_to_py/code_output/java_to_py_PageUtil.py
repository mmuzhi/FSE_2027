class PageUtil:
    def __init__(self, data, pageSize):
        self.data = data
        self.pageSize = pageSize
        self.totalItems = len(data)
        self.totalPages = (self.totalItems + self.pageSize - 1) // self.pageSize

    def getPage(self, pageNumber):
        if pageNumber < 1 or pageNumber > self.totalPages:
            return []
        startIndex = (pageNumber - 1) * self.pageSize
        endIndex = min(startIndex + self.pageSize, self.totalItems)
        return self.data[startIndex:endIndex]

    def getPageInfo(self, pageNumber):
        if pageNumber < 1 or pageNumber > self.totalPages:
            return PageInfo(0, self.pageSize, self.totalPages, self.totalItems, False, False, [])
        startIndex = (pageNumber - 1) * self.pageSize
        endIndex = min(startIndex + self.pageSize, self.totalItems)
        pageData = self.data[startIndex:endIndex]
        hasPrevious = pageNumber > 1
        hasNext = pageNumber < self.totalPages
        return PageInfo(pageNumber, self.pageSize, self.totalPages, self.totalItems, hasPrevious, hasNext, pageData)

    def search(self, keyword):
        results = [item for item in self.data if str(item).find(keyword) != -1]
        numResults = len(results)
        numPages = (numResults + self.pageSize - 1) // self.pageSize
        return SearchResult(keyword, numResults, numPages, results)


class PageInfo:
    def __init__(self, currentPage, perPage, totalPages, totalItems, hasPrevious, hasNext, data):
        self.currentPage = currentPage
        self.perPage = perPage
        self.totalPages = totalPages
        self.totalItems = totalItems
        self.hasPrevious = hasPrevious
        self.hasNext = hasNext
        self.data = data[:]  # Make a copy of the data list

    def __eq__(self, other):
        if not isinstance(other, PageInfo):
            return False
        return (self.currentPage == other.currentPage and
                self.perPage == other.perPage and
                self.totalPages == other.totalPages and
                self.totalItems == other.totalItems and
                self.hasPrevious == other.hasPrevious and
                self.hasNext == other.hasNext and
                self.data == other.data)

    def __hash__(self):
        return hash((self.currentPage, self.perPage, self.totalPages, self.totalItems, self.hasPrevious, self.hasNext, tuple(self.data)))


class SearchResult:
    def __init__(self, keyword, totalResults, totalPages, results):
        self.keyword = keyword
        self.totalResults = totalResults
        self.totalPages = totalPages
        self.results = results[:]  # Make a copy of the results list

    def __eq__(self, other):
        if not isinstance(other, SearchResult):
            return False
        return (self.totalResults == other.totalResults and
                self.totalPages == other.totalPages and
                self.keyword == other.keyword and
                self.results == other.results)

    def __hash__(self):
        return hash((self.keyword, self.totalResults, self.totalPages, tuple(self.results)))