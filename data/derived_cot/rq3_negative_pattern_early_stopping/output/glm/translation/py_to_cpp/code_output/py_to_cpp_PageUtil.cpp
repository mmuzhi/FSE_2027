#include <vector>
#include <string>
#include <map>
#include <any>
#include <algorithm>

template<typename T>
class PageUtil {
public:
    PageUtil(std::vector<T> data, int page_size)
        : data_(std::move(data)), page_size_(page_size),
          total_items_(static_cast<int>(data_.size())),
          total_pages_((total_items_ + page_size_ - 1) / page_size_) {}

    std::vector<T> get_page(int page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return {};
        }
        int start_index = (page_number - 1) * page_size_;
        int end_index = start_index + page_size_;
        if (end_index > static_cast<int>(data_.size())) {
            end_index = static_cast<int>(data_.size());
        }
        return std::vector<T>(data_.begin() + start_index, data_.begin() + end_index);
    }

    std::map<std::string, std::any> get_page_info(int page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return {};
        }
        int start_index = (page_number - 1) * page_size_;
        int end_index = std::min(start_index + page_size_, static_cast<int>(data_.size()));
        std::vector<T> page_data(data_.begin() + start_index, data_.begin() + end_index);

        std::map<std::string, std::any> page_info;
        page_info["current_page"] = page_number;
        page_info["per_page"] = page_size_;
        page_info["total_pages"] = total_pages_;
        page_info["total_items"] = total_items_;
        page_info["has_previous"] = page_number > 1;
        page_info["has_next"] = page_number < total_pages_;
        page_info["data"] = std::move(page_data);
        return page_info;
    }

    std::map<std::string, std::any> search(const std::string& keyword) const {
        std::vector<T> results;
        for (const auto& item : data_) {
            if (item_to_string(item).find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }
        int num_results = static_cast<int>(results.size());
        int num_pages = (num_results + page_size_ - 1) / page_size_;

        std::map<std::string, std::any> search_info;
        search_info["keyword"] = keyword;
        search_info["total_results"] = num_results;
        search_info["total_pages"] = num_pages;
        search_info["results"] = std::move(results);
        return search_info;
    }

private:
    std::vector<T> data_;
    int page_size_;
    int total_items_;
    int total_pages_;

    static std::string item_to_string(const T& item) {
        if constexpr (std::is_same_v<T, std::string>) {
            return item;
        } else if constexpr (std::is_arithmetic_v<T>) {
            return std::to_string(item);
        } else {
            std::ostringstream oss;
            oss << item;
            return oss.str();
        }
    }
};