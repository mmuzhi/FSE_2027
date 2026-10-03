#include <OpenXLSX.hpp>
#include <string>
#include <vector>
#include <optional>
#include <variant>
#include <algorithm>
#include <cctype>

using Object = std::variant<std::string, int, std::nullptr_t>;
using RowData = std::vector<Object>;
using DataTable = std::vector<RowData>;

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    std::optional<DataTable> readExcel(const std::string& fileName) {
        DataTable data;
        try {
            OpenXLSX::XLDocument doc;
            doc.open(fileName);
            auto wb = doc.workbook();
            auto ws = wb.worksheet(wb.worksheetNames().front());

            uint32_t rowCount = ws.rowCount();
            uint32_t colCount = ws.colCount();

            for (uint32_t r = 1; r <= rowCount; ++r) {
                RowData rowData;
                for (uint32_t c = 1; c <= colCount; ++c) {
                    auto cell = ws.cell(r, c);
                    if (cell.valueType() == OpenXLSX::XLValueType::String) {
                        rowData.push_back(cell.value().get<std::string>());
                    } else if (cell.valueType() == OpenXLSX::XLValueType::Integer) {
                        rowData.push_back(cell.value().get<int>());
                    } else if (cell.valueType() == OpenXLSX::XLValueType::Float) {
                        rowData.push_back(static_cast<int>(cell.value().get<double>()));
                    } else {
                        rowData.push_back(nullptr);
                    }
                }
                data.push_back(rowData);
            }
        } catch (...) {
            return std::nullopt;
        }
        return data;
    }

    bool writeExcel(const DataTable& data, const std::string& fileName) {
        try {
            OpenXLSX::XLDocument doc;
            doc.create(fileName);
            auto wb = doc.workbook();
            auto ws = wb.worksheet(wb.worksheetNames().front());
            ws.setName("Sheet1");

            for (size_t i = 0; i < data.size(); ++i) {
                const RowData& rowData = data[i];
                for (size_t j = 0; j < rowData.size(); ++j) {
                    auto cell = ws.cell(i + 1, j + 1);
                    const Object& value = rowData[j];
                    if (std::holds_alternative<std::string>(value)) {
                        cell.value() = std::get<std::string>(value);
                    } else if (std::holds_alternative<int>(value)) {
                        cell.value() = std::get<int>(value);
                    }
                }
            }
            doc.save();
            return true;
        } catch (...) {
            return false;
        }
    }

    std::optional<std::string> processExcelData(int N, const std::string& saveFileName) {
        auto dataOpt = readExcel(saveFileName);
        if (!dataOpt.has_value()) {
            return std::nullopt;
        }
        DataTable data = dataOpt.value();
        if (N >= static_cast<int>(data.at(0).size())) {
            return std::nullopt;
        }
        DataTable newData;
        for (const RowData& row : data) {
            RowData newRow = row;
            const Object& value = row.at(N);
            if (std::holds_alternative<std::string>(value)) {
                std::string strVal = std::get<std::string>(value);
                std::transform(strVal.begin(), strVal.end(), strVal.begin(),
                               [](unsigned char c) { return std::toupper(c); });
                newRow.push_back(strVal);
            } else {
                newRow.push_back(value);
            }
            newData.push_back(newRow);
        }
        std::string newFileName = saveFileName;
        size_t pos = newFileName.find(".xlsx");
        if (pos != std::string::npos) {
            newFileName.replace(pos, 5, "_process.xlsx");
        }
        bool success = writeExcel(newData, newFileName);
        return success ? std::optional<std::string>(newFileName) : std::nullopt;
    }
};