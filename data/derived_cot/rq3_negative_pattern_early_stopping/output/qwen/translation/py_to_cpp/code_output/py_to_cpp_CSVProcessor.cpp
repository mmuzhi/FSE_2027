#include <fstream>
#include <vector>
#include <string>
#include <cctype>
#include <algorithm>

class CSVProcessor {
public:
    int read_csv(const std::string& file_name, std::vector<std::string>& title, std::vector<std::vector<std::string>>& data) {
        std::ifstream file(file_name);
        if (!file.is_open()) {
            return 0;
        }

        std::string line;
        std::vector<std::vector<std::string>> rows;

        while (std::getline(file, line)) {
            std::vector<std::string> fields;
            parse_csv_line(line, fields);
            rows.push_back(fields);
        }

        if (rows.empty()) {
            return 0;
        }

        title = rows[0];
        data = std::vector<std::vector<std::string>>(rows.begin() + 1, rows.end());
        return 1;
    }

    int write_csv(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        std::ofstream file(file_name);
        if (!file.is_open()) {
            return 0;
        }

        for (const auto& row : data) {
            std::string formatted_row = format_csv_row(row);
            file << formatted_row << '\n';
        }
        return 1;
    }

    int process_csv_data(int N, const std::string& save_file_name) {
        std::vector<std::string> title;
        std::vector<std::vector<std::string>> data;
        if (read_csv(save_file_name, title, data) != 1) {
            return 0;
        }

        std::vector<std::string> column_data;
        for (const auto& row : data) {
            if (row.size() > static_cast<size_t>(N)) {
                column_data.push_back(row[N]);
            }
        }

        for (auto& s : column_data) {
            for (char& c : s) {
                c = std::toupper(c);
            }
        }

        std::vector<std::vector<std::string>> new_data;
        new_data.push_back(title);
        new_data.push_back(column_data);

        size_t dot_pos = save_file_name.find_last_of('.');
        std::string new_filename = save_file_name.substr(0, dot_pos) + "_process.csv";

        return write_csv(new_data, new_filename) ? 1 : 0;
    }

private:
    static void parse_csv_line(const std::string& line, std::vector<std::string>& fields) {
        bool in_quote = false;
        std::string field;
        std::string current;

        for (char c : line) {
            if (c == '"') {
                in_quote = !in_quote;
                current += c;
                continue;
            }

            if (c == ',' && !in_quote) {
                fields.push_back(current);
                current.clear();
                continue;
            }

            if (c == '\n' || c == '\r') {
                if (!current.empty()) {
                    fields.push_back(current);
                    current.clear();
                }
                break;
            }

            current += c;
        }

        if (!current.empty()) {
            fields.push_back(current);
        }
    }

    static std::string format_csv_row(const std::vector<std::string>& row) {
        std::string result;
        bool quote_needed = false;

        for (const auto& field : row) {
            if (field.find(',') != std::string::npos ||
                field.find('\n') != std::string::npos ||
                field.find('"') != std::string::npos) {
                quote_needed = true;
            }
        }

        if (quote_needed) {
            result += '"';
            for (const auto& field : row) {
                for (char c : field) {
                    if (c == '"') {
                        result += '"';
                    }
                    result += c;
                }
            }
            result += '"';
        } else {
            for (const auto& field : row) {
                result += field;
            }
        }

        return result;
    }
};