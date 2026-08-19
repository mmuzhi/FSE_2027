#include <algorithm>
#include <cstddef>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <utility>
#include <variant>
#include <vector>

template <typename T>
class PageUtil {
public:
    // Emulates Python dicts holding mixed value types.
    using InfoValue  = std::variant<long long, bool, std::string, std::vector<T>>;
    using PageInfo   = std::map<std::string, InfoValue>;
    using SearchInfo = std::map<std::string, InfoValue>;

    PageUtil(std::vector<T> data, long long page_size)
        : data_(std::move(data)),
          page_size_(page_size),
          total_items_(static_cast<long long>(data_.size())),
          total_pages_(floor_div(total_items_ + page_size_ - 1, page_size_)) {}

    // Retrieve a specific page of data (empty vector when out of range).
    std::vector<T> get_page(long long page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return {};
        }
        const std::ptrdiff_t n = static_cast<std::ptrdiff_t>(data_.size());
        std::ptrdiff_t start_index = (page_number - 1) * page_size_;
        std::ptrdiff_t end_index   = start_index + page_size_;
        // Python slicing silently clamps out-of-range indices (C++ must do it explicitly).
        start_index = std::max<std::ptrdiff_t>(0, std::min(start_index, n));
        end_index   = std::max<std::ptrdiff_t>(0, std::min(end_index, n));
        if (end_index < start_index) {
            end_index = start_index;  // Python slice with start > end yields []
        }
        return std::vector<T>(data_.begin() + start_index, data_.begin() + end_index);
    }

    // Retrieve information about a specific page (empty map when out of range).
    PageInfo get_page_info(long long page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return {};
        }
        const std::ptrdiff_t n = static_cast<std::ptrdiff_t>(data_.size());
        std::ptrdiff_t start_index = (page_number - 1) * page_size_;
        std::ptrdiff_t end_index   = start_index + page_size_;
        start_index = std::max<std::ptrdiff_t>(0, std::min(start_index, n));
        end_index   = std::max<std::ptrdiff_t>(0, std::min(end_index, n));
        if (end_index < start_index) {
            end_index = start_index;
        }
        std::vector<T> page_data(data_.begin() + start_index, data_.begin() + end_index);

        PageInfo page_info;
        page_info["current_page"] = page_number;
        page_info["per_page"]     = page_size_;
        page_info["total_pages"]  = total_pages_;
        page_info["total_items"]  = total_items_;
        page_info["has_previous"] = page_number > 1;
        page_info["has_next"]     = page_number < total_pages_;
        page_info["data"]         = std::move(page_data);
        return page_info;
    }

    // Search for items whose string form contains the keyword.
    SearchInfo search(const std::string& keyword) const {
        std::vector<T> results;
        for (const T& item : data_) {
            if (item_to_string(item).find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }
        const long long num_results = static_cast<long long>(results.size());
        const long long num_pages   = floor_div(num_results + page_size_ - 1, page_size_);

        SearchInfo search_info;
        search_info["keyword"]       = keyword;
        search_info["total_results"] = num_results;
        search_info["total_pages"]   = num_pages;
        search_info["results"]       = std::move(results);
        return search_info;
    }

private:
    // Python `//` is floor division; C++ `/` truncates. Also mimics ZeroDivisionError.
    static long long floor_div(long long a, long long b) {
        if (b == 0) {
            throw std::runtime_error("integer division or modulo by zero");
        }
        long long q = a / b;
        const long long r = a % b;
        if (r != 0 && ((r < 0) != (b < 0))) {
            --q;
        }
        return q;
    }

    // Equivalent of Python str(item).
    static std::string item_to_string(const T& item) {
        if constexpr (std::is_same_v<T, bool>) {
            return item ? "True" : "False";
        } else if constexpr (std::is_arithmetic_v<T>) {
            return std::to_string(item);
        } else {
            std::ostringstream oss;
            oss << item;
            return oss.str();
        }
    }

    std::vector<T> data_;   // must be declared before dependents
    long long page_size_;
    long long total_items_;
    long long total_pages_;
};