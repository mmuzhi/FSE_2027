#include <vector>
#include <string>
#include <unordered_map>
#include <any>
#include <stdexcept>

class PageUtil {
private:
    std::vector<std::string> data;
    int page_size;
    int total_items;
    int total_pages;

public:
    PageUtil(const std::vector<std::string>& data, int page_size)
        : data(data), page_size(page_size), total_items(data.size()) {
        total_pages = (total_items + page_size - 1) / page_size;
    }

    std::vector<std::string> get_page(int page_number) const {
        if (page_number < 1 || page_number > total_pages) {
            return {};
        }
        int start = (page_number - 1) * page_size;
        int end = start + page_size;
        if (end > total_items) end = total_items;
        return std::vector<std::string>(data.begin() + start, data.begin() + end);
    }

    std::unordered_map<std::string, std::any> get_page_info(int page_number) const {
        if (page_number < 1 || page_number > total_pages) {
            return {};
        }
        int start = (page_number - 1) * page_size;
        int end = start + page_size;
        if (end > total_items) end = total_items;
        std::vector<std::string> page_data(data.begin() + start, data.begin() + end);

        return {
            {"current_page", page_number},
            {"per_page", page_size},
            {"total_pages", total_pages},
            {"total_items", total_items},
            {"has_previous", page_number > 1},
            {"has_next", page_number < total_pages},
            {"data", page_data}
        };
    }

    std::unordered_map<std::string, std::any> search(const std::string& keyword) const {
        std::vector<std::string> results;
        for (const auto& item : data) {
            if (item.find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }
        int num_results = results.size();
        int num_pages = (num_results + page_size - 1) / page_size;

        return {
            {"keyword", keyword},
            {"total_results", num_results},
            {"total_pages", num_pages},
            {"results", results}
        };
    }
};