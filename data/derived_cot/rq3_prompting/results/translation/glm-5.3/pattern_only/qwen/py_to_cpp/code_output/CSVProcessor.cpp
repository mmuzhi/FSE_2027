/*
 * CSVProcessor: reads/writes CSV data (Python csv module default dialect:
 * comma delimiter, '"' quote char with doubling, QUOTE_MINIMAL, "\r\n" line
 * terminator) and processes the N-th column into a new "_process.csv" file.
 */

#include <cctype>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace csv_detail {

// Equivalent of Python's csv.reader (default dialect).
// Records end with '\n', '\r' or '\r\n'; a blank line yields an empty row.
inline std::vector<std::vector<std::string>> parse(const std::string& content) {
    std::vector<std::vector<std::string>> rows;
    std::vector<std::string> row;
    std::string field;
    bool in_quotes = false;
    bool started = false;  // any content/delimiter seen in current record

    size_t i = 0;
    const size_t n = content.size();
    while (i < n) {
        char c = content[i];
        if (in_quotes) {
            if (c == '"') {
                if (i + 1 < n && content[i + 1] == '"') { field += '"'; i += 2; }
                else { in_quotes = false; ++i; }
            } else { field += c; ++i; }
        } else if (c == '"' && field.empty()) {
            // quote char is special only at the start of a field
            in_quotes = true; started = true; ++i;
        } else if (c == ',') {
            row.push_back(field); field.clear(); started = true; ++i;
        } else if (c == '\n' || c == '\r') {
            i += (c == '\r' && i + 1 < n && content[i + 1] == '\n') ? 2 : 1;
            if (!started) rows.push_back(std::vector<std::string>());  // blank line -> []
            else { row.push_back(field); field.clear(); rows.push_back(row); row.clear(); }
            started = false;
        } else {
            field += c; started = true; ++i;
        }
    }
    if (in_quotes || started) {  // unterminated final record
        row.push_back(field);
        rows.push_back(row);
    }
    return rows;
}

// Equivalent of Python's csv.writer field serialization (QUOTE_MINIMAL).
inline std::string field_to_csv(const std::string& s) {
    if (s.find_first_of(",\"\r\n") == std::string::npos) return s;
    std::string out = "\"";
    for (char c : s) { out += c; if (c == '"') out += '"'; }
    out += '"';
    return out;
}

// Python-style indexing (supports negative indices, throws IndexError).
inline std::string py_index(const std::vector<std::string>& v, long long idx) {
    long long i = idx < 0 ? static_cast<long long>(v.size()) + idx : idx;
    if (i < 0 || i >= static_cast<long long>(v.size()))
        throw std::out_of_range("list index out of range");
    return v[static_cast<size_t>(i)];
}

}  // namespace csv_detail

class CSVProcessor {
public:
    CSVProcessor() {}

    // Returns {title, data}; throws if the file can't be opened or is empty
    // (Python: FileNotFoundError / StopIteration).
    std::pair<std::vector<std::string>, std::vector<std::vector<std::string>>>
    read_csv(const std::string& file_name) const {
        std::ifstream file(file_name, std::ios::binary);
        if (!file) throw std::runtime_error("FileNotFoundError: " + file_name);
        std::ostringstream ss;
        ss << file.rdbuf();
        std::vector<std::vector<std::string>> rows = csv_detail::parse(ss.str());
        if (rows.empty()) throw std::runtime_error("StopIteration");
        std::vector<std::string> title = rows.front();
        rows.erase(rows.begin());
        return std::make_pair(title, rows);
    }

    // Returns 1 on success, 0 on any failure (bare except in Python).
    int write_csv(const std::vector<std::vector<std::string>>& data,
                  const std::string& file_name) const {
        try {
            std::ofstream file(file_name, std::ios::binary | std::ios::trunc);
            if (!file) throw std::runtime_error("cannot open file");
            for (const auto& row : data) {
                if (row.size() == 1 && row[0].empty()) {
                    file << "\"\"";  // python csv writes a lone empty field as ""
                } else {
                    for (size_t j = 0; j < row.size(); ++j) {
                        if (j) file << ',';
                        file << csv_detail::field_to_csv(row[j]);
                    }
                }
                file << "\r\n";
            }
            if (!file) throw std::runtime_error("write failed");
            return 1;
        } catch (...) {
            return 0;
        }
    }

    // Keeps only the N-th (from 0) column of the data rows, upper-cases it,
    // and writes title + column into "<name before first '.'>_process.csv".
    int process_csv_data(int N, const std::string& save_file_name) const {
        std::pair<std::vector<std::string>, std::vector<std::vector<std::string>>>
            result = read_csv(save_file_name);
        const std::vector<std::string>& title = result.first;
        const std::vector<std::vector<std::string>>& data = result.second;

        std::vector<std::string> column_data;
        for (const auto& row : data) {
            std::string cell = csv_detail::py_index(row, N);  // IndexError propagates
            std::string up;
            for (char c : cell)
                up += static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
            column_data.push_back(up);
        }

        std::vector<std::vector<std::string>> new_data;
        new_data.push_back(title);
        new_data.push_back(column_data);

        std::string base = save_file_name.substr(0, save_file_name.find('.'));  // split('.')[0]
        return write_csv(new_data, base + "_process.csv");
    }
};