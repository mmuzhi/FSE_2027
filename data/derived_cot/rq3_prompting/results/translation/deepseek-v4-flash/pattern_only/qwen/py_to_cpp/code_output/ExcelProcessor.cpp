#include <xlnt/xlnt.hpp>
#include <optional>
#include <variant>
#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <cctype>
#include <cmath>
#include <charconv>
#include <stdexcept>

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    std::optional<std::vector<std::vector<xlnt::value>>> read_excel(const std::string& file_name) {
        try {
            xlnt::workbook wb;
            wb.load(file_name);
            auto ws = wb.active_sheet();
            std::vector<std::vector<xlnt::value>> data;
            for (auto row : ws.rows()) {
                std::vector<xlnt::value> row_data;
                for (auto cell : row) {
                    row_data.push_back(cell.value());
                }
                data.push_back(std::move(row_data));
            }
            return data;
        } catch (...) {
            return std::nullopt;
        }
    }

    int write_excel(const std::vector<std::vector<xlnt::value>>& data, const std::string& file_name) {
        try {
            xlnt::workbook wb;
            auto ws = wb.active_sheet();
            for (const auto& row : data) {
                ws.append(row);
            }
            wb.save(file_name);
            return 1;
        } catch (...) {
            return 0;
        }
    }

    std::variant<int, std::pair<int, std::string>> process_excel_data(int N, const std::string& save_file_name) {
        auto data_opt = read_excel(save_file_name);
        if (!data_opt.has_value()) {
            return 0;
        }

        const auto& data = data_opt.value();
        if (data.empty()) {
            throw std::out_of_range("list index out of range");
        }

        int n = N;
        int row_size = static_cast<int>(data.at(0).size());
        if (n < 0) {
            n += row_size;
            if (n < 0) {
                throw std::out_of_range("list index out of range");
            }
        } else if (n >= row_size) {
            return 0;
        }

        std::vector<std::vector<xlnt::value>> new_data;
        for (const auto& row : data) {
            std::vector<xlnt::value> new_row = row;
            const xlnt::value& cell_val = row.at(n);
            std::string str_val = python_str(cell_val);
            if (!is_digit(str_val)) {
                new_row.push_back(xlnt::value(to_upper(str_val)));
            } else {
                new_row.push_back(cell_val);
            }
            new_data.push_back(std::move(new_row));
        }

        std::string new_file_name = save_file_name.substr(0, save_file_name.find('.')) + "_process.xlsx";
        int success = write_excel(new_data, new_file_name);
        return std::pair<int, std::string>(success, new_file_name);
    }

private:
    static std::string python_str(const xlnt::value& v) {
        if (v.is_null()) return "None";
        if (v.is_boolean()) return v.get<bool>() ? "True" : "False";
        if (v.is_number()) return double_to_string(v.get<double>());
        return v.to_string();
    }

    static std::string double_to_string(double d) {
        if (std::isnan(d)) return "nan";
        if (std::isinf(d)) return d > 0 ? "inf" : "-inf";
        if (d == 0.0 && std::signbit(d)) return "-0.0";

        char buf[128];
        auto res = std::to_chars(buf, buf + sizeof(buf), d, std::chars_format::general);
        return std::string(buf, res.ptr);
    }

    static bool is_digit(const std::string& s) {
        if (s.empty()) return false;
        for (char c : s) {
            if (!std::isdigit(static_cast<unsigned char>(c))) return false;
        }
        return true;
    }

    static std::string to_upper(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(), [](unsigned char c) {
            return static_cast<char>(std::toupper(c));
        });
        return s;
    }
};