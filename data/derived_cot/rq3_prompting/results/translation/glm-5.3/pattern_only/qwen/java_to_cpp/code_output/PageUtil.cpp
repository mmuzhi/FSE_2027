#include <algorithm>
#include <cmath>
#include <cstdint>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

// Java String#hashCode (char-wise, wrapping 32-bit arithmetic)
static int javaStringHashCode(const std::string& s) {
    std::uint32_t h = 0;
    for (char c : s) {
        h = 31 * h + static_cast<std::uint8_t>(c);
    }
    return static_cast<int>(h);
}

// Java List#hashCode for List<Integer> (Integer.hashCode == value)
static int javaListHashCode(const std::vector<int>& list) {
    std::uint32_t result = 1;
    for (int item : list) {
        result = 31 * result + static_cast<std::uint32_t>(item);
    }
    return static_cast<int>(result);
}

// Emulates Java's (int) cast from double: NaN -> 0, saturates at int bounds.
static int javaDoubleToInt(double d) {
    if (std::isnan(d)) return 0;
    if (d >= 2147483647.0) return 2147483647;
    if (d <= -2147483648.0) return -2147483648;
    return static_cast<int>(d);
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
            : currentPage(currentPage),
              perPage(perPage),
              totalPages(totalPages),
              totalItems(totalItems),
              hasPrevious(hasPrevious),
              hasNext(hasNext),
              data(data) {}  // Java constructor copies the list

        bool operator==(const PageInfo& other) const {
            return currentPage == other.currentPage
                && perPage == other.perPage
                && totalPages == other.totalPages
                && totalItems == other.totalItems
                && hasPrevious == other.hasPrevious
                && hasNext == other.hasNext
                && data == other.data;
        }

        bool operator!=(const PageInfo& other) const { return !(*this == other); }

        int hashCode() const {
            std::uint32_t result = static_cast<std::uint32_t>(currentPage);
            result = 31 * result + static_cast<std::uint32_t>(perPage);
            result = 31 * result + static_cast<std::uint32_t>(totalPages);
            result = 31 * result + static_cast<std::uint32_t>(totalItems);
            result = 31 * result + (hasPrevious ? 1u : 0u);
            result = 31 * result + (hasNext ? 1u : 0u);
            result = 31 * result + static_cast<std::uint32_t>(javaListHashCode(data));
            return static_cast<int>(result);
        }
    };

    class SearchResult {
    public:
        std::string keyword;
        int totalResults;
        int totalPages;
        std::vector<int> results;

        SearchResult(std::string keyword, int totalResults, int totalPages, std::vector<int> results)
            : keyword(std::move(keyword)),
              totalResults(totalResults),
              totalPages(totalPages),
              results(std::move(results)) {}  // Java constructor copies the list

        bool operator==(const SearchResult& other) const {
            return totalResults == other.totalResults
                && totalPages == other.totalPages
                && keyword == other.keyword
                && results == other.results;
        }

        bool operator!=(const SearchResult& other) const { return !(*this == other); }

        int hashCode() const {
            std::uint32_t result = static_cast<std::uint32_t>(javaStringHashCode(keyword));
            result = 31 * result + static_cast<std::uint32_t>(totalResults);
            result = 31 * result + static_cast<std::uint32_t>(totalPages);
            result = 31 * result + static_cast<std::uint32_t>(javaListHashCode(results));
            return static_cast<int>(result);
        }
    };

    PageUtil(std::vector<int> data, int pageSize)
        : data(std::move(data)),
          pageSize(pageSize),
          totalItems(static_cast<int>(this->data.size())),
          totalPages(javaDoubleToInt(std::ceil(static_cast<double>(totalItems) / pageSize))) {}

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
            return PageInfo(0, pageSize, totalPages, totalItems, false, false, {});
        }

        int startIndex = (pageNumber - 1) * pageSize;
        int endIndex = std::min(startIndex + pageSize, totalItems);
        std::vector<int> pageData(data.begin() + startIndex, data.begin() + endIndex);

        bool hasPrevious = pageNumber > 1;
        bool hasNext = pageNumber < totalPages;

        return PageInfo(pageNumber, pageSize, totalPages, totalItems,
                        hasPrevious, hasNext, std::move(pageData));
    }

    SearchResult search(const std::string& keyword) const {
        std::vector<int> results;
        for (int item : data) {
            if (std::to_string(item).find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }

        int numResults = static_cast<int>(results.size());
        int numPages = javaDoubleToInt(std::ceil(static_cast<double>(numResults) / pageSize));

        return SearchResult(keyword, numResults, numPages, std::move(results));
    }

private:
    std::vector<int> data;
    int pageSize;
    int totalItems;
    int totalPages;
};

}  // namespace org::example