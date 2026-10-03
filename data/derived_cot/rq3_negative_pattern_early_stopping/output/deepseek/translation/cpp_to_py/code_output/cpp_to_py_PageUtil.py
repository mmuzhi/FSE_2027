from typing import List, Dict, Union, Any

class PageUtil:
    def __init__(self, data: List[int], page_size: int):
        self.data = list(data)
        self.page_size = page_size
        self.total_items = len(self.data)
        self.total_pages = (self.total_items + page_size - 1) // page_size

    def get_page(self, page_number: int) -> List[int]:
        if page_number < 1 or page_number > self.total_pages:
            return []
        start_index = (page_number - 1) * self.page_size
        end_index = start_index + self.page_size
        if end_index > self.total_items:
            end_index = self.total_items
        return self.data[start_index:end_index]

    def get_page_info(self, page_number: int) -> Dict[str, Any]:
        if page_number < 1 or page_number > self.total_pages:
            return {}
        start_index = (page_number - 1) * self.page_size
        end_index = min(start_index + self.page_size, self.total_items)
        page_data = self.data[start_index:end_index]

        return {
            "current_page": page_number,
            "per_page": self.page_size,
            "total_pages": self.total_pages,
            "total_items": self.total_items,
            "has_previous": page_number > 1,
            "has_next": page_number < self.total_pages,
            "data": page_data
        }

    def search(self, keyword: str) -> Dict[str, Any]:
        results: List[int] = []
        for item in self.data:
            if str(item).find(keyword) != -1:
                results.append(item)

        num_results = len(results)
        num_pages = (num_results + self.page_size - 1) // self.page_size

        return {
            "keyword": keyword,
            "total_results": num_results,
            "total_pages": num_pages,
            "results": results
        }