#include <OpenXLSX.hpp>
#include <string>
#include <vector>
#include <variant>
#include <optional>
#include <algorithm>
#include <cctype>
#include <utility>

class ExcelProcessor {
public:
    using CellValue = std::variant<std::string, int64_t, double>;
    using Row = std::vector<CellValue>;
    using DataTable = std::vector<Row>;

    ExcelProcessor() {}

    std::optional<DataTable> read_excel(const std::string& file_name) {
        DataTable data;
        try {
            OpenXLSX::XLDocument doc;
            doc.open(file_name);
            auto workbook = doc.workbook();
            auto sheet = workbook.worksheet(workbook.worksheetNames()[0]);

            uint32_t rowCount = sheet.rowCount();
            uint16_t colCount = sheet.columnCount();

            for (uint32_t r = 1; r <= rowCount; ++r) {
                Row row;
                bool rowHasData = false;
                for (uint16_t c = 1; c <= colCount; ++c) {
                    auto cell = sheet.cell(r, c);
                    auto type = cell.cellType();
                    if (type == OpenXLSX::XLCellType::Empty) {
                        row.push_back(std::string(""));
                    } else if (type == OpenXLSX::XLCellType::String) {
                        row.push_back(cell.value().get<std::string>());
                        rowHasData = true;
                    } else if (type == OpenXLSX::XLCellType::Integer) {
                        row.push_back(cell.value().get<int64_t>());
                        rowHasData = true;
                    } else if (type == OpenXLSX::XLCellType::Float) {
                        row.push_back(cell.value().get<double>());
                        rowHasData = true;
                    } else {
                        row.push_back(std::string(""));
                    }
                }
                if (rowHasData) {
                    data.push_back(std::move(row));
                }
            }

            doc.close();
            return data;
        } catch (...) {
            return std::nullopt;
        }
    }

    int write_excel(const DataTable& data, const std::string& file_name) {
        try {
            OpenXLSX::XLDocument doc;
            doc.create(file_name);
            auto workbook = doc.workbook();
            auto sheet = workbook.worksheet(workbook.worksheetNames()[0]);

            for (size_t r = 0; r < data.size(); ++r) {
                for (size_t c = 0; c < data[r].size(); ++c) {
                    auto cell = sheet.cell(static_cast<uint32_t>(r + 1), static_cast<uint32_t>(c + 1));
                    std::visit([&cell](auto&& arg) {
                        using T = std::decay_t<decltype(arg)>;
                        if constexpr (std::is_same_v<T, std::string>) {
                            cell.value() = arg;
                        } else if constexpr (std::is_same_v<T, int64_t>) {
                            cell.value() = arg;
                        } else if constexpr (std::is_same_v<T, double>) {
                            cell.value() = arg;
                        }
                    }, data[r][c]);
                }
            }

            doc.save();
            doc.close();
            return 1;
        } catch (...) {
            return 0;
        }
    }

    std::pair<int, std::string> process_excel_data(int N, const std::string& save_file_name) {
        auto data_opt = read_excel(save_file_name);
        if (!data_opt.has_value() || data_opt.value().empty() || N < 0 || static_cast<size_t>(N) >= data_opt.value()[0].size()) {
            return {0, ""};
        }
        auto data = std::move(data_opt.value());

        DataTable new_data;
        for (const auto& row : data) {
            Row new_row = row;

            std::string str_val;
            std::visit([&str_val](auto&& arg) {
                using T = std::decay_t<decltype(arg)>;
                if constexpr (std::is_same_v<T, std::string>) {
                    str_val = arg;
                } else if constexpr (std::is_same_v<T, int64_t>) {
                    str_val = std::to_string(arg);
                } else if constexpr (std::is_same_v<T, double>) {
                    str_val = std::to_string(arg);
                }
            }, row[N]);

            bool all_digits = !str_val.empty() &&
                std::all_of(str_val.begin(), str_val.end(), [](unsigned char ch) {
                    return std::isdigit(ch);
                });

            if (!all_digits) {
                std::string upper_val = str_val;
                std::transform(upper_val.begin(), upper_val.end(), upper_val.begin(),
                    [](unsigned char c) { return std::toupper(c); });
                new_row.push_back(upper_val);
            } else {
                new_row.push_back(row[N]);
            }
            new_data.push_back(std::move(new_row));
        }

        size_t dot_pos = save_file_name.rfind('.');
        std::string base_name = (dot_pos != std::string::npos)
            ? save_file_name.substr(0, dot_pos)
            : save_file_name;
        std::string new_file_name = base_name + "_process.xlsx";

        int success = write_excel(new_data, new_file_name);
        return {success, new_file_name};
    }
};