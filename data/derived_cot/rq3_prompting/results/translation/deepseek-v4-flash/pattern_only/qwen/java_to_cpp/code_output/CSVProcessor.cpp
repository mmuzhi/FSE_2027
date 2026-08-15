#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <cctype>
#include <stdexcept>

#ifdef _WIN32
static const char* NEWLINE = "\r\n";
#else
static const char* NEWLINE = "\n";
#endif

static std::vector<std::string> split(const std::string& s, char delim) {
    if (s.empty()) return {""};

    std::vector<std::string> result;
    std::string current;

    for (char ch : s) {
        if (ch == delim) {
            result.push_back(current);
            current.clear();
        } else {
            current.push_back(ch);
        }
    }
    result.push_back(current);

    while (!result.empty() && result.back().empty()) {
        result.pop_back();
    }

    return result;
}

static std::string join(const std::vector<std::string>& vec, char delim) {
    std::string result;
    for (size_t i = 0; i < vec.size(); ++i) {
        if (i > 0) result.push_back(delim);
        result += vec[i];
    }
    return result;
}

static bool readLine(std::ifstream& in, std::string& line) {
    line.clear();
    char c;
    bool any = false;

    while (in.get(c)) {
        any = true;
        if (c == '\n') break;
        if (c == '\r') {
            if (in.peek() == '\n') in.get();
            break;
        }
        line.push_back(c);
    }

    return any;
}

static std::string toUpper(const std::string& s) {
    std::string res = s;
    for (char& c : res) {
        c = static_cast<char>(std::toupper(static_cast<unsigned char>(c)));
    }
    return res;
}

class CSVProcessor {
public:
    void readCSV(const std::string& fileName, std::vector<std::string>& title,
                 std::vector<std::vector<std::string>>& data) {
        std::ifstream reader(fileName);
        if (!reader.is_open()) {
            throw std::ios_base::failure("Cannot open file: " + fileName);
        }

        std::string line;
        if (readLine(reader, line)) {
            std::vector<std::string> parts = split(line, ',');
            title.insert(title.end(), parts.begin(), parts.end());

            std::string lineData;
            while (readLine(reader, lineData)) {
                data.push_back(split(lineData, ','));
            }
        }

        if (reader.bad()) {
            throw std::ios_base::failure("Read error on file: " + fileName);
        }
    }

    int writeCSV(const std::vector<std::string>& title,
                 const std::vector<std::vector<std::string>>& data,
                 const std::string& fileName) {
        try {
            std::ofstream writer;
            writer.exceptions(std::ofstream::failbit | std::ofstream::badbit);
            writer.open(fileName);

            writer << join(title, ',') << NEWLINE;
            for (const auto& row : data) {
                writer << join(row, ',') << NEWLINE;
            }

            return 1;
        } catch (const std::ios_base::failure&) {
            return 0;
        }
    }

    int writeCSV(const std::vector<std::vector<std::string>>& data,
                 const std::string& fileName) {
        try {
            std::ofstream writer;
            writer.exceptions(std::ofstream::failbit | std::ofstream::badbit);
            writer.open(fileName);

            for (const auto& row : data) {
                writer << join(row, ',') << NEWLINE;
            }

            return 1;
        } catch (const std::ios_base::failure&) {
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
                columnData.push_back(toUpper(row.at(N)));
            }
        }

        std::vector<std::vector<std::string>> newData;
        newData.push_back(columnData);

        std::vector<std::string> parts = split(saveFileName, '.');
        std::string base = parts.at(0);

        return writeCSV(title, newData, base + "_process.csv");
    }
};