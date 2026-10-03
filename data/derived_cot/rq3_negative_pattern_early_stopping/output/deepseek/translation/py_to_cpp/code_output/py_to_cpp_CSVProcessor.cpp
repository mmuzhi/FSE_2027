#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>

// Helper: split a line by commas, not handling quotes or escapes.
std::vector<std::string> split_csv_line(const std::string& line) {
    std::vector<std::string> fields;
    std::stringstream ss(line);
    std::string field;
    while (std::getline(ss, field, ',')) {
        fields.push_back(field);
    }
    // If line ends with a comma, we still need to capture an empty field.
    // std::getline will not add an extra empty field for trailing comma
    if (!line.empty() && line.back() == ',') {
        fields.push_back("");
    }
    return fields;
}

class CSVProcessor {
public:
    CSVProcessor() {}

    // Read CSV file, return title row and data rows.
    // Throws std::runtime_error if file cannot be opened.
    std::pair<std::vector<std::string>, std::vector<std::vector<std::string>>>
    read_csv(const std::string& file_name) {
        std::ifstream file(file_name);
        if (!file.is_open()) {
            throw std::runtime_error("File not found: " + file_name);
        }

        std::vector<std::string> title;
        std::vector<std::vector<std::string>> data;

        std::string line;
        bool first = true;
        while (std::getline(file, line)) {
            if (first) {
                title = split_csv_line(line);
                first = false;
            } else {
                data.push_back(split_csv_line(line));
            }
        }
        return {title, data};
    }

    // Write data (vector of rows) to CSV file.
    // Returns 1 on success, 0 on failure.
    int write_csv(const std::vector<std::vector<std::string>>& data, const std::string& file_name) {
        try {
            std::ofstream file(file_name);
            if (!file.is_open()) return 0;
            for (const auto& row : data) {
                for (size_t i = 0; i < row.size(); ++i) {
                    if (i > 0) file << ",";
                    file << row[i];
                }
                file << "\n";
            }
            file.close();
            return 1;
        } catch (...) {
            return 0;
        }
    }

    // Process CSV data: keep Nth column, uppercase, write with '_process' suffix.
    int process_csv_data(int N, const std::string& save_file_name) {
        try {
            auto [title, data] = read_csv(save_file_name);
            std::vector<std::string> column_data;
            for (const auto& row : data) {
                if (N >= 0 && N < (int)row.size()) {
                    std::string val = row[N];
                    std::transform(val.begin(), val.end(), val.begin(), ::toupper);
                    column_data.push_back(val);
                } else {
                    // If N out of bounds, treat as empty string? Python would raise IndexError.
                    // To mimic Python behavior, we throw or let it crash.
                    throw std::out_of_range("Column index out of range");
                }
            }
            std::vector<std::vector<std::string>> new_data;
            new_data.push_back(title);
            new_data.push_back(column_data);
            std::string new_file_name = save_file_name.substr(0, save_file_name.find_last_of('.')) + "_process.csv";
            return write_csv(new_data, new_file_name);
        } catch (...) {
            return 0;
        }
    }
};