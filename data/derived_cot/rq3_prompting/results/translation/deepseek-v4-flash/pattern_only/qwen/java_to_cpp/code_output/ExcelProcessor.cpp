#include <xlnt/xlnt.hpp>
#include <vector>
#include <variant>
#include <string>
#include <optional>
#include <algorithm>
#include <cctype>
#include <fstream>
#include <utility>

using CellValue = std::variant<std::string, int, std::monostate>;
using RowData = std::vector<CellValue>;
using Data = std::vector<RowData>;

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    std::optional<Data> readExcel(const std::string& fileName);
    bool writeExcel(const Data& data, const std::string& fileName);
    std::optional<std::string> processExcelData(int N, const std::string& saveFileName);

private:
    static std::string replaceAll(std::string str, const std::string& from, const std::string& to);
};

std::optional<Data> ExcelProcessor::readExcel(const std::string& fileName) {
    std::ifstream file(fileName, std::ios::binary);
    if (!file.is_open()) {
        return std::nullopt;
    }
    file.close();

    Data data;
    xlnt::workbook workbook;
    try {
        workbook.load(fileName);
    } catch (const std::exception&) {
        return std::nullopt;
    }

    if (workbook.sheet_count() == 0) {
        throw std::invalid_argument("No sheet found");
    }

    xlnt::worksheet sheet = workbook.sheet_by_index(0);
    for (auto row : sheet.rows()) {
        RowData rowData;
        for (auto cell : row) {
            if (cell.data_type() == xlnt::cell_type::string) {
                rowData.emplace_back(cell.value<std::string>());
            } else if (cell.data_type() == xlnt::cell_type::number) {
                rowData.emplace_back(static_cast<int>(cell.value<double>()));
            } else {
                rowData.emplace_back(std::monostate{});
            }
        }
        data.push_back(std::move(rowData));
    }
    return data;
}

bool ExcelProcessor::writeExcel(const Data& data, const std::string& fileName) {
    try {
        xlnt::workbook workbook;
        xlnt::worksheet sheet = workbook.create_sheet("Sheet1");

        for (std::size_t i = 0; i < data.size(); ++i) {
            sheet.create_row(static_cast<xlnt::row_t>(i));
            const RowData& rowData = data[i];
            for (std::size_t j = 0; j < rowData.size(); ++j) {
                xlnt::cell cell = sheet.cell(xlnt::cell_reference(
                    static_cast<xlnt::column_t>(j + 1),
                    static_cast<xlnt::row_t>(i + 1)));
                const CellValue& value = rowData[j];
                if (std::holds_alternative<std::string>(value)) {
                    cell.value(std::get<std::string>(value));
                } else if (std::holds_alternative<int>(value)) {
                    cell.value(static_cast<double>(std::get<int>(value)));
                }
            }
        }

        workbook.save(fileName);
        return true;
    } catch (const std::exception&) {
        return false;
    }
}

std::optional<std::string> ExcelProcessor::processExcelData(int N, const std::string& saveFileName) {
    auto data = readExcel(saveFileName);
    if (!data || N >= static_cast<int>(data->at(0).size())) {
        return std::nullopt;
    }

    Data newData;
    for (const auto& row : *data) {
        RowData newRow = row;
        const CellValue& value = row.at(N);
        if (std::holds_alternative<std::string>(value)) {
            std::string s = std::get<std::string>(value);
            std::transform(s.begin(), s.end(), s.begin(),
                [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
            newRow.emplace_back(std::move(s));
        } else {
            newRow.emplace_back(value);
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

std::string ExcelProcessor::replaceAll(std::string str, const std::string& from, const std::string& to) {
    if (from.empty()) return str;
    std::size_t start = 0;
    while ((start = str.find(from, start)) != std::string::npos) {
        str.replace(start, from.length(), to);
        start += to.length();
    }
    return str;
}