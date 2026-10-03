#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <sstream>
#include <cstddef>

class PageUtil {
public:
    struct PageInfo {
        int currentPage;
        int perPage;
        int totalPages;
        int totalItems;
        bool hasPrevious;
        bool hasNext;
        std::vector<int> data;

        PageInfo(int currentPage, int perPage, int totalPages, int totalItems,
                 bool hasPrevious, bool hasNext, const std::vector<int>& data = {})
            : currentPage(currentPage), perPage(perPage), totalPages(totalPages),
              totalItems(totalItems), hasPrevious(hasPrevious), hasNext(hasNext),
              data(data) {}

        bool operator==(const PageInfo& other) const {
            return currentPage == other.currentPage &&
                   perPage == other.perPage &&
                   totalPages == other.totalPages &&
                   totalItems == other.totalItems &&
                   hasPrevious == other.hasPrevious &&
                   hasNext == other.hasNext &&
                   data == other.data;
        }
    };

    struct SearchResult {
        std::string keyword;
        int totalResults;
        int totalPages;
        std::vector<int> results;

        SearchResult(const std::string& keyword, int totalResults, int totalPages,
                     const std::vector<int>& results = {})
            : keyword(keyword), totalResults(totalResults), totalPages(totalPages),
              results(results) {}

        bool operator==(const SearchResult& other) const {
            return keyword == other.keyword &&
                   totalResults == other.totalResults &&
                   totalPages == other.totalPages &&
                   results == other.results;
        }
    };

    PageUtil(const std::vector<int>& data, int pageSize)
        : data(data), pageSize(pageSize),
          totalItems(static_cast<int>(data.size())),
          totalPages(static_cast<int>(std::ceil(static_cast<double>(totalItems) / pageSize))) {}

    std::vector<int> getPage(int pageNumber) const {
        if (pageNumber < 1 || pageNumber > totalPages) {
            return {};
        }
        int startIndex = (pageNumber - 1) * pageSize;
        int endIndex = std::min(startIndex + pageSize, totalItems);
        return std::vector<int>(data.begin() + startIndex, data.begin() + endIndex);
    }

    PageInfo getPageInfo(int pageNumber) const {
        if (pageNumber < 1 || pageNumber > totalPages) {
            return PageInfo(0, pageSize, totalPages, totalItems, false, false);
        }
        int startIndex = (pageNumber - 1) * pageSize;
        int endIndex = std::min(startIndex + pageSize, totalItems);
        std::vector<int> pageData(data.begin() + startIndex, data.begin() + endIndex);
        bool hasPrevious = pageNumber > 1;
        bool hasNext = pageNumber < totalPages;
        return PageInfo(pageNumber, pageSize, totalPages, totalItems, hasPrevious, hasNext, pageData);
    }

    SearchResult search(const std::string& keyword) const {
        std::vector<int> results;
        for (int item : data) {
            std::ostringstream oss;
            oss << item;
            if (oss.str().find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }
        int numResults = static_cast<int>(results.size());
        int numPages = static_cast<int>(std::ceil(static_cast<double>(numResults) / pageSize));
        return SearchResult(keyword, numResults, numPages, results);
    }

private:
    std::vector<int> data;
    int pageSize;
    int totalItems;
    int totalPages;
};