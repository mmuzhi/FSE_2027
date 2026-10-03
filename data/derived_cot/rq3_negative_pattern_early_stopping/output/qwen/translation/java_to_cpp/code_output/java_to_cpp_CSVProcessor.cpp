#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <cctype>
#include <algorithm>

// Helper function to split a string by commas
std::vector<std::string> split(const std::string& s) {
    std::vector<std::string> tokens;
    std::string token;
    std::istringstream iss(s);
    while (std::getline(iss, token, ',')) {
        tokens.push_back(token);
    }
    return tokens;
}

class CSVProcessor {
public:
    void readCSV(const std::string& fileName, std::vector<std::string>& title, std::vector<std::vector<std::string>>& data) {
        std::ifstream file(fileName);
        if (!file.is_open()) {
            throw std::runtime_error("Could not open file: " + fileName);
        }

        std::string firstLine;
        if (std::getline(file, firstLine)) {
            std::vector<std::string> tokens = split(firstLine);
            title.reserve(title.size() + tokens.size());
            for (const auto& token : tokens) {
                title.push_back(token);
            }

            std::vector<std::string> currentRow;
            while (std::getline(file, firstLine)) {
                currentRow = split(firstLine);
                data.push_back(currentRow);
            }
        }
    }

    int writeCSV(const std::vector<std::string>& title, const std::vector<std::vector<std::string>>& data, const std::string& fileName) {
        std::ofstream file(fileName);
        if (!file.is_open()) {
            return 0;
        }

        for (size_t i = 0; i < title.size(); ++i) {
            if (i > 0) file << ",";
            file << title[i];
        }
        file << '\n';

        for (const auto& row : data) {
            for (size_t i = 0; i < row.size(); ++i) {
                if (i > 0) file << ",";
                file << row[i];
            }
            file << '\n';
        }
        return 1;
    }

    int writeCSV(const std::vector<std::vector<std::string>>& data, const std::string& fileName) {
        std::ofstream file(fileName);
        if (!file.is_open()) {
            return 0;
        }

        for (const auto& row : data) {
            for (size_t i = 0; i < row.size(); ++i) {
                if (i > 0) file << ",";
                file << row[i];
            }
            file << '\n';
        }
        return 1;
    }

    int processCSVData(int N, const std::string& saveFileName) {
        std::vector<std::string> title;
        std::vector<std::vector<std::string>> data;

        try {
            readCSV(saveFileName, title, data);
        } catch (const std::exception& e) {
            throw std::runtime_error("Error reading CSV: " + std::string(e.what()));
        }

        std::vector<std::string> columnData;
        for (const auto& row : data) {
            if (static_cast<size_t>(N) < row.size()) {
                std::string cell = row[N];
                std::transform(cell.begin(), cell.end(), cell.begin(), [](unsigned char c) { return std::toupper(c); });
                columnData.push_back(cell);
            }
        }

        std::vector<std::vector<std::string>> newData;
        newData.push_back(columnData);

        size_t lastDot = saveFileName.find_last_of('.');
        std::string baseName = (lastDot != std::string::npos) ? saveFileName.substr(0, lastDot) : saveFileName;
        std::string newFileName = baseName + "_process.csv";

        try {
            return writeCSV(title, newData, newFileName);
        } catch (...) {
            return 0;
        }
    }
};