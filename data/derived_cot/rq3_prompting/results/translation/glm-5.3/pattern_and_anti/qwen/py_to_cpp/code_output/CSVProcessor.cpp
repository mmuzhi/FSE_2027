#include <cctype>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class CSVProcessor {
public:
    CSVProcessor() {}

    // Behavior equivalent of Python:
    //   title, data = read_csv(file_name)  -> tuple (first row, remaining rows)
    // Raises if the file cannot be opened or is empty (StopIteration analog).
    std::pair<std::vector<std::string>, std::vector<std::vector<std::string>>>
    read_csv(const std::string& file_name) {
        std::ifstream file(file_name, std::ios::binary);
        if (!file.is_open()) {
            throw std::runtime_error("[Errno 2] No such file or directory: '" + file_name + "'");
        }
        std::string content((std::istreambuf_iterator<char>(file)), std::istreambuf_iterator<char>());
        std::vector<std::vector<std::string>> rows = parse_csv(content);
        if (rows.empty()) {
            throw std::runtime_error("StopIteration");
        }
        std::vector<std::string> title = rows.front();
        std::vector<std::vector<std::string>> data(rows.begin() + 1, rows.end());
        return {title, data};
    }

    // Returns 1 on success, 0 on any failure (mirrors bare `except: return 0`).
    int write_csv(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        try {
            std::ofstream file(file_name, std::ios::binary | std::ios::trunc);
            if (!file.is_open()) {
                throw std::runtime_error("unable to open file");
            }
            for (const auto& row : data) {
                for (size_t i = 0; i < row.size(); ++i) {
                    if (i > 0) file << ',';
                    file << quote_field(row[i]);
                }
                file << "\r\n"; // csv.writer default lineterminator
            }
            return 1;
        } catch (...) {
            return 0;
        }
    }

    int process_csv_data(int N, const std::string& save_file_name) {
        auto result = read_csv(save_file_name);
        const std::vector<std::string>& title = result.first;
        const std::vector<std::vector<std::string>>& data = result.second;

        std::vector<std::string> column_data;
        for (const auto& row : data) {
            column_data.push_back(py_index(row, N)); // IndexError analog (supports negative N)
        }
        for (auto& s : column_data) {
            for (auto& ch : s) ch = static_cast<char>(std::toupper(static_cast<unsigned char>(ch)));
        }

        std::vector<std::vector<std::string>> new_data = {title, column_data};
        // Python: save_file_name.split('.')[0] + '_process.csv'
        size_t dot = save_file_name.find('.');
        std::string base = save_file_name.substr(0, dot); // whole string if no '.'
        return write_csv(new_data, base + "_process.csv");
    }

private:
    // csv.reader-like parser: comma delimiter, '"' quotechar, '""' escape,
    // fields may span lines, blank line -> empty row.
    static std::vector<std::vector<std::string>> parse_csv(const std::string& content) {
        std::vector<std::vector<std::string>> rows;
        std::vector<std::string> row;
        std::string field;
        bool in_quotes = false;
        size_t i = 0;
        const size_t n = content.size();
        while (i < n) {
            char c = content[i];
            if (in_quotes) {
                if (c == '"') {
                    if (i + 1 < n && content[i + 1] == '"') { field += '"'; i += 2; }
                    else { in_quotes = false; ++i; }
                } else { field += c; ++i; }
            } else if (c == '"') {
                in_quotes = true; ++i;
            } else if (c == ',') {
                row.push_back(field); field.clear(); ++i;
            } else if (c == '\r' || c == '\n') {
                if (c == '\r' && i + 1 < n && content[i + 1] == '\n') ++i;
                ++i;
                row.push_back(field); field.clear();
                rows.push_back(row); row.clear();
            } else {
                field += c; ++i;
            }
        }
        if (!field.empty() || !row.empty()) {
            row.push_back(field);
            rows.push_back(row);
        }
        return rows;
    }

    // csv.writer QUOTE_MINIMAL: quote only if field contains , " \r or \n.
    static std::string quote_field(const std::string& s) {
        if (s.find_first_of(",\"\r\n") == std::string::npos) return s;
        std::string out = "\"";
        for (char c : s) {
            if (c == '"') out += "\"\"";
            else out += c;
        }
        out += "\"";
        return out;
    }

    // Python list indexing semantics, including negative indices; throws on out of range.
    static const std::string& py_index(const std::vector<std::string>& row, int N) {
        long idx = N < 0 ? static_cast<long>(row.size()) + N : static_cast<long>(N);
        if (idx < 0 || idx >= static_cast<long>(row.size())) {
            throw std::out_of_range("list index out of range");
        }
        return row[static_cast<size_t>(idx)];
    }
};