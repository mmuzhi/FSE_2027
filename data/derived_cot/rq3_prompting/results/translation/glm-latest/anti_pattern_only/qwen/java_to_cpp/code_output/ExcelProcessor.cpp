// Requires the xlnt library (C++ analog of Apache POI for .xlsx files):
//   https://github.com/tfussell/xlnt
#include <xlnt/xlnt.hpp>

#include <algorithm>
#include <cctype>
#include <exception>
#include <optional>
#include <string>
#include <variant>
#include <vector>

namespace org {
namespace example {

// Java's List<List<Object>> holds String, Integer, or null per cell.
// std::nullopt          <-> null
// std::variant entry    <-> Object value (String or Integer)
using CellValue = std::optional<std::variant<std::string, int>>;
using SheetData = std::vector<std::vector<CellValue>>;

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    // Returns std::nullopt on an I/O failure (Java: returns null on IOException).
    std::optional<SheetData> readExcel(const std::string& fileName) {
        SheetData data;
        xlnt::workbook workbook;
        try {
            workbook.load(fileName);
        } catch (const std::exception&) {
            return std::nullopt; // IOException -> null
        }
        xlnt::worksheet sheet = workbook.sheet_by_index(0);
        for (auto row : sheet.rows()) {
            std::vector<CellValue> rowData;
            for (auto cell : row) {
                switch (cell.data_type()) {
                    case xlnt::cell::type::shared_string:
                    case xlnt::cell::type::inline_string:
                        rowData.emplace_back(cell.to_string());
                        break;
                    case xlnt::cell::type::number:
                        // (int) cell.getNumericCellValue(): double truncated to int
                        rowData.emplace_back(static_cast<int>(cell.value().as<double>()));
                        break;
                    default:
                        rowData.emplace_back(std::nullopt);
                        break;
                }
            }
            data.push_back(std::move(rowData));
        }
        return data;
    }

    bool writeExcel(const SheetData& data, const std::string& fileName) {
        try {
            xlnt::workbook workbook;
            // A fresh xlnt workbook already contains one empty sheet; use it as "Sheet1".
            xlnt::worksheet sheet = workbook.active_sheet();
            sheet.title("Sheet1");
            for (std::size_t i = 0; i < data.size(); ++i) {
                const std::vector<CellValue>& rowData = data[i];
                for (std::size_t j = 0; j < rowData.size(); ++j) {
                    // 1-based access creates the cell, like row.createCell(j)
                    xlnt::cell cell = sheet.cell(i + 1, j + 1);
                    const CellValue& value = rowData[j];
                    if (value.has_value()) {
                        if (const auto* str = std::get_if<std::string>(&*value)) {
                            // infer_type = false: keep it a string like setCellValue(String)
                            cell.value(*str, false);
                        } else if (const auto* num = std::get_if<int>(&*value)) {
                            cell.value(*num);
                        }
                        // null (or other) values: cell exists but stays blank, as in Java
                    }
                }
            }
            workbook.save(fileName);
            return true;
        } catch (const std::exception&) {
            return false; // IOException -> false
        }
    }

    // Returns std::nullopt on failure (Java: returns null).
    std::optional<std::string> processExcelData(int N, const std::string& saveFileName) {
        std::optional<SheetData> data = readExcel(saveFileName);
        // Short-circuits like Java; .at(0) throws std::out_of_range on an empty sheet,
        // mirroring the uncaught IndexOutOfBoundsException of data.get(0).
        if (!data.has_value() || N >= static_cast<int>(data->at(0).size())) {
            return std::nullopt;
        }
        SheetData newData;
        for (const std::vector<CellValue>& row : *data) {
            std::vector<CellValue> newRow(row); // copy like new ArrayList<>(row)
            const CellValue& value = row.at(N); // .at(N) mirrors row.get(N) throwing
            if (value.has_value() && std::holds_alternative<std::string>(*value)) {
                newRow.push_back(toUpperCase(std::get<std::string>(*value)));
            } else {
                newRow.push_back(value);
            }
            newData.push_back(std::move(newRow));
        }
        std::string newFileName = replaceAll(saveFileName, ".xlsx", "_process.xlsx");
        bool success = writeExcel(newData, newFileName);
        if (success) {
            return newFileName;
        }
        return std::nullopt;
    }

private:
    static std::string toUpperCase(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(),
                       [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
        return s;
    }

    // Java's String.replace(CharSequence, CharSequence): replace every literal occurrence
    static std::string replaceAll(std::string str, const std::string& from, const std::string& to) {
        if (from.empty()) {
            return str;
        }
        std::string::size_type pos = 0;
        while ((pos = str.find(from, pos)) != std::string::npos) {
            str.replace(pos, from.length(), to);
            pos += to.length();
        }
        return str;
    }
};

} // namespace example
} // namespace org