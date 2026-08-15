#include <algorithm>
#include <any>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <utility>
#include <vector>

template<typename T>
std::string to_string_item(const T& value) {
    if constexpr (std::is_same_v<T, bool>) {
        return value ? "True" : "False";
    } else if constexpr (std::is_same_v<T, std::string>) {
        return value;
    } else if constexpr (std::is_same_v<T, const char*>) {
        return std::string(value);
    } else if constexpr (std::is_floating_point_v<T>) {
        std::ostringstream oss;
        oss << value;
        std::string s = oss.str();
        if (s.find('.') == std::string::npos &&
            s.find('e') == std::string::npos &&
            s.find('E') == std::string::npos) {
            s += ".0";
        }
        return s;
    } else {
        std::ostringstream oss;
        oss << value;
        return oss.str();
    }
}

template<typename T>
class PageUtil {
public:
    PageUtil(std::vector<T> data, int page_size)
        : data_(std::move(data)),
          page_size_(page_size),
          total_items_(static_cast<int>(data_.size())) {
        if (page_size_ == 0) {
            throw std::invalid_argument("division by zero");
        }
        total_pages_ = floor_div(total_items_ + page_size_ - 1, page_size_);
    }

    std::vector<T> get_page(int page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return {};
        }
        int start_index = (page_number - 1) * page_size_;
        int end_index = start_index + page_size_;
        return slice_data(start_index, end_index);
    }

    std::map<std::string, std::any> get_page_info(int page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return {};
        }
        int start_index = (page_number - 1) * page_size_;
        int end_index = std::min(start_index + page_size_, total_items_);
        std::vector<T> page_data = slice_data(start_index, end_index);

        std::map<std::string, std::any> page_info;
        page_info["current_page"] = page_number;
        page_info["per_page"] = page_size_;
        page_info["total_pages"] = total_pages_;
        page_info["total_items"] = total_items_;
        page_info["has_previous"] = page_number > 1;
        page_info["has_next"] = page_number < total_pages_;
        page_info["data"] = page_data;
        return page_info;
    }

    std::map<std::string, std::any> search(const std::string& keyword) const {
        std::vector<T> results;
        for (const auto& item : data_) {
            if (to_string_item(item).find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }
        int num_results = static_cast<int>(results.size());
        int num_pages = floor_div(num_results + page_size_ - 1, page_size_);

        std::map<std::string, std::any> search_info;
        search_info["keyword"] = keyword;
        search_info["total_results"] = num_results;
        search_info["total_pages"] = num_pages;
        search_info["results"] = results;
        return search_info;
    }

private:
    std::vector<T> data_;
    int page_size_;
    int total_items_;
    int total_pages_;

    static int floor_div(int a, int b) {
        int q = a / b;
        int r = a % b;
        if (r != 0 && ((r > 0) != (b > 0))) {
            --q;
        }
        return q;
    }

    std::vector<T> slice_data(int start, int end) const {
        int n = total_items_;
        if (start < 0) start = std::max(0, n + start);
        if (end < 0) end = std::max(0, n + end);
        if (start > n) start = n;
        if (end > n) end = n;
        if (start >= end) return {};
        return std::vector<T>(data_.begin() + start, data_.begin() + end);
    }
};