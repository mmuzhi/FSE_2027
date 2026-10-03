#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <stdexcept>

class CSVProcessor {
public:
    void readCSV(const std::string& fileName, std::vector<std::string>& title, std::vector<std::vector<std::string>>& data) {
        std::ifstream reader(fileName);
        if (!reader.is_open()) {
            throw std::runtime_error("Cannot open file: " + fileName);
        }

        std::string line;
        if (std::getline(reader, line)) {
            title = split(line, ',');
            while (std::getline(reader, line)) {
                data.push_back(split(line, ','));
            }
        }
        reader.close();
    }

    int writeCSV(const std::vector<std::string>& title, const std::vector<std::vector<std::string>>& data, const std::string& fileName) {
        try {
            std::ofstream writer(fileName);
            if (!writer.is_open()) {
                return 0;
            }
            writer << join(title, ",") << "\n";
            for (const auto& row : data) {
                writer << join(row, ",") << "\n";
            }
            writer.close();
            return 1;
        } catch (...) {
            return 0;
        }
    }

    int writeCSV(const std::vector<std::vector<std::string>>& data, const std::string& fileName) {
        try {
            std::ofstream writer(fileName);
            if (!writer.is_open()) {
                return 0;
            }
            for (const auto& row : data) {
                writer << join(row, ",") << "\n";
            }
            writer.close();
            return 1;
        } catch (...) {
            return 0;
        }
    }

    int processCSVData(int N, const std::string& saveFileName) {
        std::vector<std::string> title;
        std::vector<std::vector<std::string>> data;
        readCSV(saveFileName, title, data);

        std::vector<std::string> columnData;
        for (const auto& row : data) {
            if (N < static_cast<int>(row.size())) {
                std::string cell = row[N];
                std::transform(cell.begin(), cell.end(), cell.begin(), ::toupper);
                columnData.push_back(cell);
            }
        }

        std::vector<std::vector<std::string>> newData;
        newData.push_back(columnData);

        std::string baseName = saveFileName;
        size_t dotPos = baseName.rfind('.');
        if (dotPos != std::string::npos) {
            baseName = baseName.substr(0, dotPos);
        }
        return writeCSV(title, newData, baseName + "_process.csv");
    }

private:
    static std::vector<std::string> split(const std::string& s, char delimiter) {
        std::vector<std::string> tokens;
        std::string token;
        std::istringstream tokenStream(s);
        while (std::getline(tokenStream, token, delimiter)) {
            tokens.push_back(token);
        }
        // Handle trailing empty strings matching Java's split behavior
        // Java's split with one-char regex discards trailing empty strings.
        // But also empty string input gives one empty token.
        if (s.empty()) {
            tokens.clear();
            tokens.push_back("");
        } else if (!s.empty() && s.back() == delimiter) {
            while (!tokens.empty() && tokens.back().empty()) {
                tokens.pop_back();
            }
        }
        return tokens;
    }

    static std::string join(const std::vector<std::string>& strings, const std::string& delimiter) {
        std::ostringstream oss;
        for (size_t i = 0; i < strings.size(); ++i) {
            if (i != 0) oss << delimiter;
            oss << strings[i];
        }
        return oss.str();
    }
};