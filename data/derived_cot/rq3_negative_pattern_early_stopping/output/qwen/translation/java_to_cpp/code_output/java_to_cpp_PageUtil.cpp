#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <optional>
#include <sstream>

class PageUtil {
private:
    std::vector<int> data;
    int pageSize;
    int totalItems;
    int totalPages;

public:
    PageUtil(const std::vector<int>& data, int pageSize) {
        this->data = data;
        this->pageSize = pageSize;
        this->totalItems = data.size();
        totalPages = (totalItems + pageSize - 1) / pageSize;
    }

    std::vector<int> getPage(int pageNumber) {
        if (pageNumber < 1 || pageNumber > totalPages) {
            return std::vector<int>();
        }

        int startIndex = (pageNumber - 1) * pageSize;
        int endIndex = std::min(startIndex + pageSize, totalItems);
        return std::vector<int>(data.begin() + startIndex, data.begin() + endIndex);
    }

    struct PageInfo {
        int currentPage;
        int perPage;
        int totalPages;
        int totalItems;
        bool hasPrevious;
        bool hasNext;
        std::vector<int> data;

        PageInfo(int currentPage, int perPage, int totalPages, int totalItems, bool hasPrevious, bool hasNext, const std::vector<int>& data)
            : currentPage(currentPage), perPage(perPage), totalPages(totalPages), totalItems(totalItems),
              hasPrevious(hasPrevious), hasNext(hasNext), data(data) {}
    };

    PageInfo getPageInfo(int pageNumber) {
        if (pageNumber < 1 || pageNumber > totalPages) {
            return PageInfo(0, pageSize, totalPages, totalItems, false, false, std::vector<int>());
        }

        int startIndex = (pageNumber - 1) * pageSize;
        int endIndex = std::min(startIndex + pageSize, totalItems);
        std::vector<int> pageData(data.begin() + startIndex, data.begin() + endIndex);

        bool hasPrevious = (pageNumber > 1);
        bool hasNext = (pageNumber < totalPages);

        return PageInfo(pageNumber, pageSize, totalPages, totalItems, hasPrevious, hasNext, std::move(pageData));
    }

    struct SearchResult {
        std::string keyword;
        int totalResults;
        int totalPages;
        std::vector<int> results;

        SearchResult(const std::string& keyword, int totalResults, int totalPages, const std::vector<int>& results)
            : keyword(keyword), totalResults(totalResults), totalPages(totalPages), results(results) {}
    };

    SearchResult search(const std::string& keyword) {
        std::vector<int> results;
        for (int item : data) {
            std::ostringstream oss;
            oss << item;
            std::string itemStr = oss.str();
            if (itemStr.find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }

        int numResults = results.size();
        int numPages = (numResults + pageSize - 1) / pageSize;

        return SearchResult(keyword, numResults, numPages, std::move(results));
    };
};