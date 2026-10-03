#include <OpenXLSX/OpenXLSX.hpp>
#include <string>
#include <vector>
#include <tuple>
#include <cctype>
#include <algorithm>
#include <stdexcept>

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    // Read data from Excel file. Returns a vector of rows, each row is a vector of strings.
    // The method reads the active sheet and returns all cells' display values.
    std::vector<std::vector<std::string>> read_excel(const std::string& file_name) {
        std::vector<std::vector<std::string>> data;
        try {
            OpenXLSX::XLDocument doc;
            doc.open(file_name);
            auto wks = doc.workbook().activeSheet();
            auto lastRow = wks.rowCount();
            auto lastCol = wks.columnCount();
            for (uint64_t row = 1; row <= lastRow; ++row) {
                std::vector<std::string> rowData;
                for (uint64_t col = 1; col <= lastCol; ++col) {
                    auto cell = wks.cell(row, col);
                    if (cell.value().type() == OpenXLSX::XLValueType::Empty) {
                        rowData.emplace_back("");
                    } else {
                        rowData.emplace_back(cell.value().get<std::string>());
                    }
                }
                data.push_back(rowData);
            }
            doc.close();
            return data;
        } catch (...) {
            return {}; // return empty vector on failure
        }
    }

    // Write data to an Excel file.
    // Returns 1 on success, 0 on failure.
    int write_excel(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        try {
            OpenXLSX::XLDocument doc;
            doc.create(file_name);
            auto wks = doc.workbook().activeSheet();
            for (size_t row = 0; row < data.size(); ++row) {
                for (size_t col = 0; col < data[row].size(); ++col) {
                    wks.cell(row+1, col+1).value() = data[row][col];
                }
            }
            doc.save();
            doc.close();
            return 1;
        } catch (...) {
            return 0;
        }
    }

    // Process Excel data: read file, add a new column with transformed values.
    // Returns a tuple (success, output_file_name).
    std::tuple<int, std::string> process_excel_data(int N, const std::string& save_file_name) {
        auto data = read_excel(save_file_name);
        if (data.empty() || data[0].empty() || N < 0 || static_cast<size_t>(N) >= data[0].size()) {
            return std::make_tuple(0, "");
        }
        std::vector<std::vector<std::string>> new_data;
        new_data.reserve(data.size());
        for (const auto& row : data) {
            std::vector<std::string> new_row = row; // copy original
            const std::string& cell_val = row[N];
            bool is_digit = !cell_val.empty() && std::all_of(cell_val.begin(), cell_val.end(), ::isdigit);
            if (!is_digit) {
                std::string upper = cell_val;
                std::transform(upper.begin(), upper.end(), upper.begin(), ::toupper);
                new_row.push_back(upper);
            } else {
                new_row.push_back(cell_val);
            }
            new_data.push_back(new_row);
        }
        // Generate output file name: remove extension, add '_process.xlsx'
        std::string new_file_name = save_file_name;
        auto dot_pos = new_file_name.rfind('.');
        if (dot_pos != std::string::npos) {
            new_file_name = new_file_name.substr(0, dot_pos) + "_process.xlsx";
        } else {
            new_file_name += "_process.xlsx";
        }
        int success = write_excel(new_data, new_file_name);
        return std::make_tuple(success, new_file_name);
    }
};