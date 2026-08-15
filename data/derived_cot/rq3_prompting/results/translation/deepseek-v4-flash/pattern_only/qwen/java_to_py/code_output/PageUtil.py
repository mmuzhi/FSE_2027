import math
from collections.abc import MutableSequence


def _java_hash_string(s):
    h = 0
    utf16 = s.encode('utf-16-be')
    for i in range(0, len(utf16), 2):
        h = (31 * h + (utf16[i] << 8 | utf16[i + 1])) & 0xFFFFFFFF
    if h >= 2**31:
        h -= 2**32
    return h


def _java_hash_list(lst):
    h = 1
    for e in lst:
        h = (31 * h + e) & 0xFFFFFFFF
    if h >= 2**31:
        h -= 2**32
    return h


class _SubList(MutableSequence):
    def __init__(self, data, start, end):
        self._data = data
        self._start = start
        self._end = end

    def __len__(self):
        return self._end - self._start

    def _normalize_index(self, index):
        if not isinstance(index, int):
            raise TypeError("list indices must be integers")
        if index < 0 or index >= len(self):
            raise IndexError("list index out of range")
        return index

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if step != 1:
                return [self[i] for i in range(start, stop, step)]
            return _SubList(self._data, self._start + start, self._start + stop)
        idx = self._normalize_index(index)
        return self._data[self._start + idx]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if step != 1:
                indices = list(range(start, stop, step))
                value_list = list(value)
                if len(indices) != len(value_list):
                    raise ValueError(
                        "attempt to assign sequence of size {} to extended slice of size {}".format(
                            len(value_list), len(indices)
                        )
                    )
                for i, v in zip(indices, value_list):
                    self._data[self._start + i] = v
                return
            value_list = list(value)
            self._data[self._start + start:self._start + stop] = value_list
            self._end = self._start + start + len(value_list)
            return
        idx = self._normalize_index(index)
        self._data[self._start + idx] = value

    def __delitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(len(self))
            if step != 1:
                indices = list(range(start, stop, step))
                for i in sorted(indices, reverse=True):
                    del self._data[self._start + i]
                self._end -= len(indices)
                return
            del self._data[self._start + start:self._start + stop]
            self._end -= (stop - start)
            return
        idx = self._normalize_index(index)
        del self._data[self._start + idx]
        self._end -= 1

    def insert(self, index, value):
        if index < 0 or index > len(self):
            raise IndexError("list index out of range")
        self._data.insert(self._start + index, value)
        self._end += 1

    def pop(self, index=None):
        if index is None:
            index = len(self) - 1
        v = self[index]
        del self[index]
        return v

    def sort(self, *, key=None, reverse=False):
        sub = self._data[self._start:self._end]
        sub.sort(key=key, reverse=reverse)
        self._data[self._start:self._end] = sub

    def __eq__(self, other):
        if isinstance(other, _SubList):
            return list(self) == list(other)
        if isinstance(other, list):
            return list(self) == other
        return NotImplemented

    def __hash__(self):
        return _java_hash_list(self)


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
        return (
            self.currentPage == obj.currentPage and
            self.perPage == obj.perPage and
            self.totalPages == obj.totalPages and
            self.totalItems == obj.totalItems and
            self.hasPrevious == obj.hasPrevious and
            self.hasNext == obj.hasNext and
            self.data == obj.data
        )

    def __hash__(self):
        result = self.currentPage
        result = (31 * result + self.perPage) & 0xFFFFFFFF
        result = (31 * result + self.totalPages) & 0xFFFFFFFF
        result = (31 * result + self.totalItems) & 0xFFFFFFFF
        result = (31 * result + (1 if self.hasPrevious else 0)) & 0xFFFFFFFF
        result = (31 * result + (1 if self.hasNext else 0)) & 0xFFFFFFFF
        result = (31 * result + _java_hash_list(self.data)) & 0xFFFFFFFF
        if result >= 2**31:
            result -= 2**32
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
        return (
            self.totalResults == obj.totalResults and
            self.totalPages == obj.totalPages and
            self.keyword == obj.keyword and
            self.results == obj.results
        )

    def __hash__(self):
        result = _java_hash_string(self.keyword)
        result = (31 * result + self.totalResults) & 0xFFFFFFFF
        result = (31 * result + self.totalPages) & 0xFFFFFFFF
        result = (31 * result + _java_hash_list(self.results)) & 0xFFFFFFFF
        if result >= 2**31:
            result -= 2**32
        return result


class PageUtil:
    PageInfo = PageInfo
    SearchResult = SearchResult

    def __init__(self, data, page_size):
        self.data = data
        self.page_size = page_size
        self.total_items = len(data)
        self.total_pages = int(math.ceil(self.total_items / page_size))

    def get_page(self, page_number):
        if page_number < 1 or page_number > self.total_pages:
            return []
        start_index = (page_number - 1) * self.page_size
        end_index = min(start_index + self.page_size, self.total_items)
        return _SubList(self.data, start_index, end_index)

    def get_page_info(self, page_number):
        if page_number < 1 or page_number > self.total_pages:
            return PageInfo(0, self.page_size, self.total_pages, self.total_items, False, False, [])
        start_index = (page_number - 1) * self.page_size
        end_index = min(start_index + self.page_size, self.total_items)
        page_data = _SubList(self.data, start_index, end_index)
        has_previous = page_number > 1
        has_next = page_number < self.total_pages
        return PageInfo(
            page_number,
            self.page_size,
            self.total_pages,
            self.total_items,
            has_previous,
            has_next,
            page_data,
        )

    def search(self, keyword):
        results = [item for item in self.data if keyword in str(item)]
        num_results = len(results)
        num_pages = int(math.ceil(num_results / self.page_size))
        return SearchResult(keyword, num_results, num_pages, results)