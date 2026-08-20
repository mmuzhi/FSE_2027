#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <optional>
#include <algorithm>
#include <cctype>
#include <utility>

class ExcelProcessor {
public:
    ExcelProcessor() {}

    std::optional<std::vector<std::vector<std::string>>> read_excel(const std::string& file_name) {
        std::vector<std::vector<std::string>> data;
        try {
            std::ifstream file(file_name);
            if (!file.is_open()) {
                return std::nullopt;
            }
            std::string line;
            while (std::getline(file, line)) {
                std::vector<std::string> row;
                std::stringstream ss(line);
                std::string cell;
                while (std::getline(ss, cell, ',')) {
                    row.push_back(cell);
                }
                data.push_back(row);
            }
            file.close();
            return data;
        } catch (...) {
            return std::nullopt;
        }
    }

    int write_excel(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        try {
            std::ofstream file(file_name);
            if (!file.is_open()) {
                return 0;
            }
            for (const auto& row : data) {
                for (size_t i = 0; i < row.size(); i++) {
                    if (i > 0) file << ",";
                    file << row[i];
                }
                file << "\n";
            }
            file.close();
            return 1;
        } catch (...) {
            return 0;
        }
    }

    std::pair<int, std::string> process_excel_data(int N, const std::string& save_file_name) {
        auto data_opt = read_excel(save_file_name);
        if (!data_opt.has_value()) {
            return {0, ""};
        }
        auto data = data_opt.value();
        if (data.empty() || N < 0 || N >= static_cast<int>(data[0].size())) {
            return {0, ""};
        }
        std::vector<std::vector<std::string>> new_data;
        for (const auto& row : data) {
            std::vector<std::string> new_row = row;
            std::string val = (N < static_cast<int>(row.size())) ? row[N] : "";
            if (!is_all_digits(val)) {
                std::string upper_val = val;
                std::transform(upper_val.begin(), upper_val.end(), upper_val.begin(),
                               [](unsigned char c) { return std::toupper(c); });
                new_row.push_back(upper_val);
            } else {
                new_row.push_back(val);
            }
            new_data.push_back(new_row);
        }
        std::string base_name = save_file_name.substr(0, save_file_name.find('.'));
        std::string new_file_name = base_name + "_process.xlsx";
        int success = write_excel(new_data, new_file_name);
        return {success, new_file_name};
    }

private:
    static bool is_all_digits(const std::string& s) {
        if (s.empty()) return false;
        for (char c : s) {
            if (!std::isdigit(static_cast<unsigned char>(c))) return false;
        }
        return true;
    }
};