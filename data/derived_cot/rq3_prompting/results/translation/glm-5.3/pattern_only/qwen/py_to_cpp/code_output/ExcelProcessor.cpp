#include <algorithm>
#include <cctype>
#include <optional>
#include <string>
#include <utility>
#include <variant>
#include <vector>
#include <xlnt/xlnt.hpp>

/*
 * A class for processing excel files, including reading and writing excel data,
 * as well as processing specific operations and saving as a new excel file.
 */
class ExcelProcessor {
public:
    ExcelProcessor() = default;

    /*
     * Reading data from Excel files
     * :param file_name: Excel file name to read
     * :return: rows of the active sheet, or std::nullopt on any failure
     *          (Python: returns None when any exception occurs)
     */
    std::optional<std::vector<std::vector<std::string>>>
    read_excel(const std::string& file_name) const {
        std::vector<std::vector<std::string>> data;
        try {
            xlnt::workbook workbook;
            workbook.load(file_name);
            xlnt::worksheet sheet = workbook.active_sheet();
            for (const auto& row : sheet.rows(false)) { // values only, keep empties
                std::vector<std::string> cells;
                cells.reserve(row.length());
                for (const auto& cell : row)
                    cells.push_back(cell.to_string());
                data.push_back(std::move(cells));
            }
            return data;
        } catch (...) {
            return std::nullopt;
        }
    }

    /*
     * Write data to the specified Excel file
     * :param data: Data to be written
     * :param file_name: Excel file name to write to
     * :return: 1 represents successful writing, 0 represents failed writing
     */
    int write_excel(const std::vector<std::vector<std::string>>& data,
                    const std::string& file_name) const {
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

    /*
     * Change the specified column in the Excel file to uppercase
     * :param N: The serial number of the column that want to change
     * :param save_file_name: source file name
     * :return: on success a (int, str) pair -- the return value of write_excel
     *          and the saved file name; on failure just the int 0
     *          (mirrored via std::variant, since Python returns a bare 0)
     */
    std::variant<int, std::pair<int, std::string>>
    process_excel_data(int N, const std::string& save_file_name) const {
        auto data = read_excel(save_file_name);
        // Python raises IndexError on data[0] when data is empty; at(0) mirrors this
        if (!data.has_value() || N >= static_cast<int>(data->at(0).size()))
            return 0;

        std::vector<std::vector<std::string>> new_data;
        new_data.reserve(data->size());
        for (const auto& row : *data) {
            std::vector<std::string> new_row(row); // list(row[:])
            const std::string& value = row.at(static_cast<std::size_t>(N));
            if (!is_digit_str(value))                 // not str(row[N]).isdigit()
                new_row.push_back(to_upper(value));   // str(row[N]).upper()
            else
                new_row.push_back(value);             // original value
            new_data.push_back(std::move(new_row));
        }

        std::string new_file_name = base_name(save_file_name) + "_process.xlsx";
        int success = write_excel(new_data, new_file_name);
        return std::make_pair(success, new_file_name);
    }

private:
    // Equivalent of Python's str.isdigit(): False for empty strings
    static bool is_digit_str(const std::string& s) {
        return !s.empty() && std::all_of(s.begin(), s.end(),
                                         [](unsigned char c) { return std::isdigit(c) != 0; });
    }

    static std::string to_upper(std::string s) {
        std::transform(s.begin(), s.end(), s.begin(),
                       [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
        return s;
    }

    // Equivalent of save_file_name.split('.')[0]
    static std::string base_name(const std::string& name) {
        std::string::size_type pos = name.find('.');
        return pos == std::string::npos ? name : name.substr(0, pos);
    }
};