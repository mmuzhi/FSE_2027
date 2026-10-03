#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <stdexcept>

class CSVProcessor {
public:
    CSVProcessor() {}

    std::pair<std::vector<std::string>, std::vector<std::vector<std::string>>> read_csv(const std::string& file_name) {
        std::vector<std::vector<std::string>> data;
        std::ifstream file(file_name);
        if (!file.is_open()) {
            throw std::runtime_error("Could not open file: " + file_name);
        }

        std::string line;

        std::vector<std::string> title;
        if (std::getline(file, line)) {
            title = parse_csv_line(strip_cr(line));
        }

        while (std::getline(file, line)) {
            data.push_back(parse_csv_line(strip_cr(line)));
        }

        return {title, data};
    }

    int write_csv(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        try {
            std::ofstream file(file_name);
            if (!file.is_open()) {
                return 0;
            }
            for (const auto& row : data) {
                write_csv_row(file, row);
                file << "\n";
            }
            return 1;
        } catch (...) {
            return 0;
        }
    }

    int process_csv_data(int N, const std::string& save_file_name) {
        auto [title, data] = read_csv(save_file_name);
        std::vector<std::string> column_data;
        for (const auto& row : data) {
            column_data.push_back(to_upper(row.at(N)));
        }
        std::vector<std::vector<std::string>> new_data = {title, column_data};

        size_t dot_pos = save_file_name.find('.');
        std::string base_name = (dot_pos == std::string::npos) ? save_file_name : save_file_name.substr(0, dot_pos);
        std::string new_file_name = base_name + "_process.csv";

        return write_csv(new_data, new_file_name);
    }

private:
    std::string strip_cr(const std::string& s) {
        if (!s.empty() && s.back() == '\r') {
            return s.substr(0, s.size() - 1);
        }
        return s;
    }

    std::vector<std::string> parse_csv_line(const std::string& line) {
        std::vector<std::string> result;
        std::string field;
        bool in_quotes = false;

        for (size_t i = 0; i < line.size(); ++i) {
            char c = line[i];
            if (in_quotes) {
                if (c == '"') {
                    if (i + 1 < line.size() && line[i + 1] == '"') {
                        field += '"';
                        ++i;
                    } else {
                        in_quotes = false;
                    }
                } else {
                    field += c;
                }
            } else {
                if (c == '"') {
                    in_quotes = true;
                } else if (c == ',') {
                    result.push_back(field);
                    field.clear();
                } else {
                    field += c;
                }
            }
        }
        result.push_back(field);
        return result;
    }

    void write_csv_row(std::ofstream& file, const std::vector<std::string>& row) {
        for (size_t i = 0; i < row.size(); ++i) {
            if (i > 0) file << ",";
            if (needs_quoting(row[i])) {
                file << "\"" << escape_quotes(row[i]) << "\"";
            } else {
                file << row[i];
            }
        }
    }

    bool needs_quoting(const std::string& field) {
        return field.find(',') != std::string::npos ||
               field.find('"') != std::string::npos ||
               field.find('\n') != std::string::npos;
    }

    std::string escape_quotes(const std::string& field) {
        std::string result;
        for (char c : field) {
            if (c == '"') {
                result += "\"\"";
            } else {
                result += c;
            }
        }
        return result;
    }

    std::string to_upper(const std::string& s) {
        std::string result = s;
        std::transform(result.begin(), result.end(), result.begin(), [](unsigned char c) {
            return std::toupper(c);
        });
        return result;
    }
};