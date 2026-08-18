#include <algorithm>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class PageUtil {
public:
    struct PageInfo {
        int current_page;
        int per_page;
        int total_pages;
        int total_items;
        bool has_previous;
        bool has_next;
        std::vector<int> data;
    };

    struct SearchInfo {
        std::string keyword;
        int total_results;
        int total_pages;
        std::vector<int> results;
    };

    PageUtil(std::vector<int> data, int page_size)
        : data_(std::move(data)), page_size_(page_size) {
        // Python raises ZeroDivisionError on `// page_size` when page_size == 0.
        if (page_size_ == 0) {
            throw std::invalid_argument("integer division or modulo by zero");
        }
        total_items_ = static_cast<int>(data_.size());
        total_pages_ = (total_items_ + page_size_ - 1) / page_size_;
    }

    // Returns the items on the given page; empty vector for out-of-range pages.
    std::vector<int> get_page(int page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return {};
        }
        int start_index = (page_number - 1) * page_size_;
        int end_index = start_index + page_size_;
        // Python slicing clamps the end index to the sequence length.
        end_index = std::min(end_index, total_items_);
        return std::vector<int>(data_.begin() + start_index, data_.begin() + end_index);
    }

    // Returns page information; std::nullopt for out-of-range pages (analog of {}).
    std::optional<PageInfo> get_page_info(int page_number) const {
        if (page_number < 1 || page_number > total_pages_) {
            return std::nullopt;
        }

        int start_index = (page_number - 1) * page_size_;
        int end_index = std::min(start_index + page_size_, total_items_);
        std::vector<int> page_data(data_.begin() + start_index, data_.begin() + end_index);

        PageInfo page_info;
        page_info.current_page = page_number;
        page_info.per_page = page_size_;
        page_info.total_pages = total_pages_;
        page_info.total_items = total_items_;
        page_info.has_previous = page_number > 1;
        page_info.has_next = page_number < total_pages_;
        page_info.data = std::move(page_data);
        return page_info;
    }

    SearchInfo search(const std::string& keyword) const {
        SearchInfo search_info;
        search_info.keyword = keyword;

        for (const auto& item : data_) {
            // Equivalent of `keyword in str(item)`; empty keyword matches everything.
            if (std::to_string(item).find(keyword) != std::string::npos) {
                search_info.results.push_back(item);
            }
        }

        search_info.total_results = static_cast<int>(search_info.results.size());
        search_info.total_pages =
            (search_info.total_results + page_size_ - 1) / page_size_;
        return search_info;
    }

private:
    std::vector<int> data_;
    int page_size_;
    int total_items_;
    int total_pages_;
};