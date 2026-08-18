#include <algorithm>
#include <cctype>
#include <optional>
#include <string>
#include <utility>
#include <vector>
#include <xlnt/xlnt.hpp>

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    // Reading data from Excel files.
    // Returns cell data (as strings) or std::nullopt on any failure (Python: None).
    std::optional<std::vector<std::vector<std::string>>> read_excel(const std::string& file_name) {
        std::vector<std::vector<std::string>> data;
        try {
            xlnt::workbook workbook;
            workbook.load(file_name);
            xlnt::worksheet sheet = workbook.active_sheet();
            for (auto row : sheet.rows(false)) {
                std::vector<std::string> row_data;
                for (auto cell : row)
                    row_data.push_back(cell.to_string());
                data.push_back(std::move(row_data));
            }
            return data;
        } catch (...) {
            return std::nullopt;
        }
    }

    // Write data to the specified Excel file.
    // Returns 1 on success, 0 on failure.
    int write_excel(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        try {
            xlnt::workbook workbook;
            xlnt::worksheet sheet = workbook.active_sheet();
            for (const auto& row : data)
                sheet.append(row);
            workbook.save(file_name);
            return 1;
        } catch (...) {
            return 0;
        }
    }

    // Change the specified column in the Excel file to uppercase (appended per row).
    // Returns (write_excel result, saved file name); {0, ""} on invalid input/short column.
    std::pair<int, std::string> process_excel_data(int N, const std::string& save_file_name) {
        auto data = read_excel(save_file_name);
        if (!data.has_value() || N >= static_cast<int>(data->at(0).size()))
            return {0, ""};
        std::vector<std::vector<std::string>> new_data;
        for (const auto& row : *data) {
            std::vector<std::string> new_row = row; // list(row[:])
            // Python-style index (negative counts from the end); at() mirrors IndexError.
            std::size_t idx = (N < 0)
                ? static_cast<std::size_t>(static_cast<std::ptrdiff_t>(row.size()) + N)
                : static_cast<std::size_t>(N);
            const std::string& value = row.at(idx);
            bool is_digit = !value.empty() && std::all_of(value.begin(), value.end(),
                [](unsigned char c) { return std::isdigit(c) != 0; });
            if (!is_digit) {
                std::string upper = value;
                std::transform(upper.begin(), upper.end(), upper.begin(),
                    [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
                new_row.push_back(std::move(upper));
            } else {
                new_row.push_back(value);
            }
            new_data.push_back(std::move(new_row));
        }
        // Equivalent of save_file_name.split('.')[0] + '_process.xlsx'
        std::string new_file_name =
            save_file_name.substr(0, save_file_name.find('.')) + "_process.xlsx";
        int success = write_excel(new_data, new_file_name);
        return {success, new_file_name};
    }
};