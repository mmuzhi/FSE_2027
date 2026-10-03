#include <vector>
#include <string>
#include <sstream>
#include <map>

template <typename T>
class PageUtil {
private:
    std::vector<T> data;
    int page_size;
    long total_items;
    long total_pages;

    struct PageInfo {
        int current_page;
        int per_page;
        long total_pages;
        long total_items;
        bool has_previous;
        bool has_next;
        std::vector<T> data;
    };

    struct SearchInfo {
        std::string keyword;
        long total_results;
        long total_pages;
        std::vector<T> results;
    };

public:
    PageUtil(const std::vector<T>& data, int page_size) 
        : data(data), page_size(page_size) {
        total_items = data.size();
        total_pages = (total_items + page_size - 1) / page_size;
    }

    std::vector<T> get_page(int page_number) {
        if (page_number < 1 || page_number > total_pages) {
            return std::vector<T>();
        }
        int start_index = (page_number - 1) * page_size;
        int end_index = start_index + page_size;
        return std::vector<T>(data.begin() + start_index, data.begin() + end_index);
    }

    PageInfo get_page_info(int page_number) {
        if (page_number < 1 || page_number > total_pages) {
            return PageInfo{0, 0, 0, 0, false, false, {}};
        }
        int start_index = (page_number - 1) * page_size;
        int end_index = start_index + page_size;
        if (end_index > total_items) {
            end_index = total_items;
        }
        std::vector<T> page_data(data.begin() + start_index, data.begin() + end_index);

        return PageInfo{
            page_number,
            page_size,
            total_pages,
            total_items,
            page_number > 1,
            page_number < total_pages,
            page_data
        };
    }

    SearchInfo search(const std::string& keyword) {
        std::vector<T> results;
        for (const T& item : data) {
            std::stringstream ss;
            ss << item;
            if (ss.str().find(keyword) != std::string::npos) {
                results.push_back(item);
            }
        }
        long num_results = results.size();
        long num_pages = (num_results + page_size - 1) / page_size;

        return SearchInfo{
            keyword,
            num_results,
            num_pages,
            results
        };
    }
};