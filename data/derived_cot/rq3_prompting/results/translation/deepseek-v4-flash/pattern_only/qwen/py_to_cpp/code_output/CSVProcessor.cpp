#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cctype>
#include <stdexcept>
#include <utility>

class CSVProcessor {
public:
    std::pair<std::vector<std::string>, std::vector<std::vector<std::string>>> read_csv(const std::string& file_name) {
        std::ifstream in(file_name);
        if (!in.is_open()) {
            throw std::runtime_error("File not found: " + file_name);
        }
        std::stringstream buffer;
        buffer << in.rdbuf();
        std::string content = normalize_newlines(buffer.str());

        std::vector<std::vector<std::string>> rows = parse_csv(content);
        if (rows.empty()) {
            throw std::runtime_error("No rows");
        }

        std::vector<std::string> title = rows[0];
        std::vector<std::vector<std::string>> data(rows.begin() + 1, rows.end());
        return std::make_pair(title, data);
    }

    int write_csv(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        try {
            std::ofstream out(file_name, std::ios::binary);
            if (!out.is_open()) {
                return 0;
            }
            for (const auto& row : data) {
                for (size_t i = 0; i < row.size(); ++i) {
                    if (i > 0) out << ',';
                    out << escape_csv_field(row[i]);
                }
                out << "\r\n";
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
            size_t idx = N >= 0 ? static_cast<size_t>(N) : static_cast<size_t>(row.size() + N);
            column_data.push_back(row.at(idx));
        }

        for (auto& s : column_data) {
            for (auto& c : s) {
                c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
            }
        }

        std::vector<std::vector<std::string>> new_data;
        new_data.push_back(title);
        new_data.push_back(column_data);

        std::string base = save_file_name;
        size_t dot = base.find('.');
        if (dot != std::string::npos) {
            base = base.substr(0, dot);
        }
        std::string new_file = base + "_process.csv";

        return write_csv(new_data, new_file);
    }

private:
    static std::string normalize_newlines(const std::string& s) {
        std::string result;
        result.reserve(s.size());
        for (size_t i = 0; i < s.size(); ++i) {
            if (s[i] == '\r') {
                result += '\n';
                if (i + 1 < s.size() && s[i + 1] == '\n') {
                    ++i;
                }
            } else {
                result += s[i];
            }
        }
        return result;
    }

    static std::vector<std::vector<std::string>> parse_csv(const std::string& s) {
        std::vector<std::vector<std::string>> rows;
        std::vector<std::string> row;
        std::string field;
        bool in_quotes = false;
        bool field_started = false;
        size_t i = 0;

        while (i < s.size()) {
            char c = s[i];

            if (in_quotes) {
                if (c == '"') {
                    if (i + 1 < s.size() && s[i + 1] == '"') {
                        field += '"';
                        i += 2;
                        continue;
                    } else {
                        in_quotes = false;
                        i += 1;
                        continue;
                    }
                } else {
                    field += c;
                    field_started = true;
                    i += 1;
                    continue;
                }
            } else {
                if (c == '"' && field.empty()) {
                    in_quotes = true;
                    field_started = true;
                    i += 1;
                    continue;
                }

                if (c == ',') {
                    row.push_back(field);
                    field.clear();
                    field_started = true;
                    i += 1;
                    continue;
                }

                if (c == '\r' || c == '\n') {
                    if (row.empty() && field.empty() && !field_started) {
                        rows.push_back(std::vector<std::string>());
                    } else {
                        row.push_back(field);
                        rows.push_back(row);
                    }
                    row.clear();
                    field.clear();
                    field_started = false;
                    i += 1;
                    continue;
                }

                field += c;
                field_started = true;
                i += 1;
            }
        }

        if (in_quotes) {
            throw std::runtime_error("unexpected end of data");
        }

        if (field_started || !row.empty() || !field.empty()) {
            row.push_back(field);
            rows.push_back(row);
        }

        return rows;
    }

    static std::string escape_csv_field(const std::string& field) {
        bool need_quote = false;
        for (char c : field) {
            if (c == ',' || c == '"' || c == '\r' || c == '\n') {
                need_quote = true;
                break;
            }
        }

        if (!need_quote) {
            return field;
        }

        std::string escaped;
        escaped += '"';
        for (char c : field) {
            if (c == '"') {
                escaped += '"';
            }
            escaped += c;
        }
        escaped += '"';
        return escaped;
    }
};