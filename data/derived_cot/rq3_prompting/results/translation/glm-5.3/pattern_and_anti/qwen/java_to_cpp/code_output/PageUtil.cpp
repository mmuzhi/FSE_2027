#include <cmath>
#include <cstdint>
#include <string>
#include <vector>

namespace org {
namespace example {

// Helpers replicating Java's hashCode arithmetic (32-bit wraparound)
static int32_t javaCombine(int32_t result, int32_t value) {
    uint32_t r = static_cast<uint32_t>(result);
    r = 31u * r + static_cast<uint32_t>(value);
    return static_cast<int32_t>(r);
}

static int32_t javaStringHash(const std::string& s) {
    int32_t h = 0;
    for (unsigned char c : s) {
        h = javaCombine(h, static_cast<int32_t>(c));
    }
    return h;
}

static int32_t javaListHash(const std::vector<int>& v) {
    int32_t result = 1;
    for (int x : v) {
        result = javaCombine(result, x); // Integer.hashCode(x) == x
    }
    return result;
}

class PageUtil {
public:
    class PageInfo {
    public:
        int currentPage;
        int perPage;
        int totalPages;
        int totalItems;
        bool hasPrevious;
        bool hasNext;
        std::vector<int> data;

        PageInfo(int currentPage, int perPage, int totalPages, int totalItems,
                 bool hasPrevious, bool hasNext, std::vector<int> data)
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

        bool operator!=(const PageInfo& other) const {
            return !(*this == other);
        }

        int32_t hashCode() const {
            int32_t result = currentPage;
            result = javaCombine(result, perPage);
            result = javaCombine(result, totalPages);
            result = javaCombine(result, totalItems);
            result = javaCombine(result, hasPrevious ? 1 : 0);
            result = javaCombine(result, hasNext ? 1 : 0);
            result = javaCombine(result, javaListHash(data));
            return result;
        }
    };

    class SearchResult {
    public:
        std::string keyword;
        int totalResults;
        int totalPages;
        std::vector<int> results;

        SearchResult(std::string keyword, int totalResults, int totalPages,
                    std::vector<int> results)
            : keyword(keyword), totalResults(totalResults), totalPages(totalPages),
              results(results) {}

        bool operator==(const SearchResult& other) const {
            return totalResults == other.totalResults &&
                   totalPages == other.totalPages &&
                   keyword == other.keyword &&
                   results == other.results;
        }

        bool operator!=(const SearchResult& other) const {
            return !(*this == other);
        }

        int32_t hashCode() const {
            int32_t result = javaStringHash(keyword);
            result = javaCombine(result, totalResults);
            result = javaCombine(result, totalPages);
            result = javaCombine(result, javaListHash(results));
            return result;
        }
    };

private:
    std::vector<int> data;
    int pageSize;
    int totalItems;
    int totalPages;

public:
    PageUtil(std::vector<int> data, int pageSize)
        : data(data), pageSize(pageSize), totalItems(static_cast<int>(data.size())) {
        totalPages = static_cast<int>(std::ceil(static_cast<double>(totalItems) / pageSize));
    }

    std::vector<int> getPage(int pageNumber) const {
        if (pageNumber < 1 || pageNumber > totalPages) {
            return std::vector<int>();
        }

        int startIndex = (pageNumber - 1) * pageSize;
        int endIndex = std::min(startIndex + pageSize, totalItems);
        return std::vector<int>(data.begin() + startIndex, data.begin() + endIndex);
    }

    PageInfo getPageInfo(int pageNumber) const {
        if (pageNumber < 1 || pageNumber > totalPages) {
            return PageInfo(0, pageSize, totalPages, totalItems, false, false, std::vector<int>());
        }

        int startIndex = (pageNumber - 1) * pageSize;
        int endIndex = std::min(startIndex + pageSize, totalItems);
        std::vector<int> pageData(data.begin() + startIndex, data.begin() + endIndex);

        bool hasPrevious = pageNumber > 1;
        bool hasNext = pageNumber < totalPages;

        return PageInfo(
            pageNumber,
            pageSize,
            totalPages,
            totalItems,
            hasPrevious,
            hasNext,
            pageData
        );
    }

    SearchResult search(const std::string& keyword) const {
        std::vector<int> results;
        for (int item : data) {
            if (std::to_string(item).find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }

        int numResults = static_cast<int>(results.size());
        int numPages = static_cast<int>(std::ceil(static_cast<double>(numResults) / pageSize));

        return SearchResult(
            keyword,
            numResults,
            numPages,
            results
        );
    }
};

} // namespace example
} // namespace org