#include <OpenXLSX/OpenXLSX.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <any>
#include <optional>
#include <fstream>
#include <algorithm>
#include <cctype>

class ExcelProcessor {
public:
    ExcelProcessor() = default;

    // Read first sheet of .xlsx file; returns nullopt on I/O error
    std::optional<std::vector<std::vector<std::any>>> readExcel(const std::string& fileName) {
        try {
            OpenXLSX::XLDocument doc;
            doc.open(fileName);
            auto sheet = doc.workbook().sheet(1); // first sheet (1-based)
            auto rows = sheet.rows();

            std::vector<std::vector<std::any>> data;
            for (auto& row : rows) {
                std::vector<std::any> rowData;
                for (auto& cell : row) {
                    auto cellType = cell.valueType();
                    switch (cellType) {
                        case OpenXLSX::XLValueType::String: {
                            rowData.emplace_back(cell.value().get<std::string>());
                            break;
                        }
                        case OpenXLSX::XLValueType::Integer: {
                            rowData.emplace_back(cell.value().get<int>());
                            break;
                        }
                        case OpenXLSX::XLValueType::Float: {
                            // Java uses (int) which truncates toward zero
                            double d = cell.value().get<double>();
                            rowData.emplace_back(static_cast<int>(d));
                            break;
                        }
                        default: {
                            // null (empty std::any)
                            rowData.emplace_back(std::any{});
                            break;
                        }
                    }
                }
                data.push_back(std::move(rowData));
            }
            doc.close();
            return data;
        }
        catch (const std::exception&) {
            return std::nullopt;
        }
    }

    // Write data (vector of rows) to a new .xlsx file
    bool writeExcel(const std::vector<std::vector<std::any>>& data, const std::string& fileName) {
        try {
            OpenXLSX::XLDocument doc;
            doc.create(fileName);
            auto sheet = doc.workbook().sheet(1);

            for (size_t i = 0; i < data.size(); ++i) {
                auto row = sheet.row(static_cast<OpenXLSX::XLRowIndex>(i + 1)); // 1-based row index
                const auto& rowData = data[i];
                for (size_t j = 0; j < rowData.size(); ++j) {
                    auto cell = row.cell(static_cast<OpenXLSX::XLColumnIndex>(j + 1)); // 1-based column index
                    const auto& value = rowData[j];
                    if (value.type() == typeid(std::string)) {
                        cell.value() = std::any_cast<std::string>(value);
                    }
                    else if (value.type() == typeid(int)) {
                        cell.value() = std::any_cast<int>(value);
                    }
                    // else cell remains empty (default)
                }
            }
            doc.save();
            doc.close();
            return true;
        }
        catch (const std::exception&) {
            return false;
        }
    }

    // Process data: read, modify column N, write to new file
    std::optional<std::string> processExcelData(int N, const std::string& saveFileName) {
        auto dataOpt = readExcel(saveFileName);
        if (!dataOpt) {
            return std::nullopt;
        }
        const auto& data = dataOpt.value();
        if (data.empty() || N >= static_cast<int>(data[0].size())) {
            return std::nullopt;
        }

        std::vector<std::vector<std::any>> newData;
        for (const auto& row : data) {
            std::vector<std::any> newRow = row;  // copy
            const auto& value = row[N];
            if (value.type() == typeid(std::string)) {
                std::string str = std::any_cast<std::string>(value);
                std::transform(str.begin(), str.end(), str.begin(), ::toupper);
                newRow.push_back(std::move(str));
            }
            else {
                newRow.push_back(value); // includes empty/integer
            }
            newData.push_back(std::move(newRow));
        }

        // Replace ".xlsx" with "_process.xlsx" (works only if extension exists)
        std::string newFileName = saveFileName;
        size_t pos = newFileName.rfind(".xlsx");
        if (pos != std::string::npos) {
            newFileName.replace(pos, 5, "_process.xlsx");
        } else {
            // fallback if no .xlsx extension
            newFileName += "_process.xlsx";
        }

        bool success = writeExcel(newData, newFileName);
        if (success) {
            return newFileName;
        }
        return std::nullopt;
    }
};