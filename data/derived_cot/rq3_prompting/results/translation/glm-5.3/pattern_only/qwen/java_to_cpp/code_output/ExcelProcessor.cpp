#include <xlnt/xlnt.hpp>

#include <algorithm>
#include <cctype>
#include <optional>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>

namespace org::example {

class ExcelProcessor
{
public:
    // Object-equivalent: String -> std::string, Integer -> int, null -> std::nullopt
    using CellValue = std::optional<std::variant<std::string, int>>;
    using Table = std::vector<std::vector<CellValue>>;

    ExcelProcessor() = default;

    // Returns std::nullopt on I/O failure (Java: returns null on IOException)
    std::optional<Table> readExcel(const std::string &fileName)
    {
        Table data;
        try
        {
            xlnt::workbook workbook;
            workbook.load(fileName); // throws on missing/invalid file (≈ IOException)

            xlnt::worksheet sheet = workbook.sheet_by_index(0);
            for (const auto &row : sheet.rows(false)) // include blank rows/cells like POI iteration
            {
                std::vector<CellValue> rowData;
                for (const auto &cell : row)
                {
                    switch (cell.data_type())
                    {
                    case xlnt::cell::type::string:
                        rowData.emplace_back(cell.to_string());
                        break;
                    case xlnt::cell::type::number:
                        // Java: (int) cast on double -> truncation toward zero (static_cast matches)
                        rowData.emplace_back(static_cast<int>(cell.to_number<double>()));
                        break;
                    default:
                        rowData.emplace_back(std::nullopt); // blank/boolean/error/formula -> null
                        break;
                    }
                }
                data.push_back(std::move(rowData));
            }
        }
        catch (const std::exception &)
        {
            return std::nullopt;
        }
        return data;
    }

    bool writeExcel(const Table &data, const std::string &fileName)
    {
        try
        {
            xlnt::workbook workbook;
            xlnt::worksheet sheet = workbook.active_sheet();
            sheet.title("Sheet1");

            for (std::size_t i = 0; i < data.size(); ++i)
            {
                const std::vector<CellValue> &rowData = data[i];
                for (std::size_t j = 0; j < rowData.size(); ++j)
                {
                    xlnt::cell cell = sheet.cell(i + 1, j + 1); // xlnt is 1-based; POI is 0-based
                    const CellValue &value = rowData[j];
                    if (value.has_value() && std::holds_alternative<std::string>(*value))
                    {
                        cell.value(std::get<std::string>(*value));
                    }
                    else if (value.has_value() && std::holds_alternative<int>(*value))
                    {
                        cell.value(std::get<int>(*value));
                    }
                    // null / other types: cell created but left blank, as in Java
                }
            }
            workbook.save(fileName);
            return true;
        }
        catch (const std::exception &)
        {
            return false;
        }
    }

    // Returns std::nullopt on failure/null result (Java: returns null String)
    std::optional<std::string> processExcelData(int N, const std::string &saveFileName)
    {
        std::optional<Table> data = readExcel(saveFileName);
        // .at(0) throws std::out_of_range when empty, mirroring IndexOutOfBoundsException
        if (!data.has_value() || N >= static_cast<int>(data->at(0).size()))
        {
            return std::nullopt;
        }

        Table newData;
        newData.reserve(data->size());
        for (const std::vector<CellValue> &row : *data)
        {
            std::vector<CellValue> newRow(row); // copy of the row, like new ArrayList<>(row)
            // .at(N) throws std::out_of_range on short rows, mirroring IndexOutOfBoundsException
            const CellValue &value = row.at(static_cast<std::size_t>(N));
            if (value.has_value() && std::holds_alternative<std::string>(*value))
            {
                newRow.emplace_back(toUpperCase(std::get<std::string>(*value)));
            }
            else
            {
                newRow.emplace_back(value);
            }
            newData.push_back(std::move(newRow));
        }

        std::string newFileName = replaceAll(saveFileName, ".xlsx", "_process.xlsx");
        bool success = writeExcel(newData, newFileName);
        return success ? std::optional<std::string>(newFileName) : std::nullopt;
    }

private:
    static std::string toUpperCase(const std::string &s)
    {
        std::string result = s;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
        return result;
    }

    // Java String.replace replaces ALL literal occurrences
    static std::string replaceAll(std::string str, const std::string &from, const std::string &to)
    {
        if (from.empty()) return str;
        std::size_t pos = 0;
        while ((pos = str.find(from, pos)) != std::string::npos)
        {
            str.replace(pos, from.length(), to);
            pos += to.length();
        }
        return str;
    }
};

} // namespace org::example