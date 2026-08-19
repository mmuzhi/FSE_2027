#include <algorithm>
#include <cctype>
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace org_example {

class CSVProcessor {
public:
    // Java: readCSV appends to title/data and propagates IOException on open/read failure.
    void readCSV(const std::string& fileName,
                 std::vector<std::string>& title,
                 std::vector<std::vector<std::string>>& data) {
        std::ifstream reader(fileName);
        if (!reader) {
            throw std::runtime_error("IOException: cannot open file " + fileName);
        }

        std::string line;
        if (std::getline(reader, line)) {
            stripCR(line); // BufferedReader.readLine strips \n and \r\n
            std::vector<std::string> tokens = splitJava(line, ',');
            title.insert(title.end(), tokens.begin(), tokens.end()); // addAll semantics

            std::string lineData;
            while (std::getline(reader, lineData)) {
                stripCR(lineData);
                data.push_back(splitJava(lineData, ','));
            }
        }
    }

    int writeCSV(const std::vector<std::string>& title,
                 const std::vector<std::vector<std::string>>& data,
                 const std::string& fileName) {
        std::ofstream writer(fileName); // FileWriter truncates existing file
        if (!writer) return 0;

        writer << join(title, ',') << "\n";
        for (const std::vector<std::string>& row : data) {
            writer << join(row, ',') << "\n";
        }
        return writer.good() ? 1 : 0;
    }

    int writeCSV(const std::vector<std::vector<std::string>>& data,
                 const std::string& fileName) {
        std::ofstream writer(fileName);
        if (!writer) return 0;

        for (const std::vector<std::string>& row : data) {
            writer << join(row, ',') << "\n";
        }
        return writer.good() ? 1 : 0;
    }

    int processCSVData(int N, const std::string& saveFileName) {
        std::vector<std::string> title;
        std::vector<std::vector<std::string>> data;
        readCSV(saveFileName, title, data);

        std::vector<std::string> columnData;
        for (const std::vector<std::string>& row : data) {
            // Java compares int N < int size(); guard negative N against size_t wraparound.
            if (N >= 0 && static_cast<size_t>(N) < row.size()) {
                columnData.push_back(toUpperJava(row[static_cast<size_t>(N)]));
            }
        }

        std::vector<std::vector<std::string>> newData;
        newData.push_back(columnData);

        return writeCSV(title, newData, baseName(saveFileName) + "_process.csv");
    }

private:
    static void stripCR(std::string& s) {
        if (!s.empty() && s.back() == '\r') s.pop_back();
    }

    // Java String.split(",") with limit 0: keeps interior empty fields,
    // drops trailing empty fields, and returns {s} when no delimiter present.
    static std::vector<std::string> splitJava(const std::string& s, char delim) {
        std::vector<std::string> tokens;
        if (s.find(delim) == std::string::npos) {
            tokens.push_back(s);
            return tokens;
        }
        std::string token;
        std::istringstream stream(s);
        while (std::getline(stream, token, delim)) {
            tokens.push_back(token);
        }
        while (!tokens.empty() && tokens.back().empty()) {
            tokens.pop_back();
        }
        return tokens;
    }

    // Java String.join(",", parts)
    static std::string join(const std::vector<std::string>& parts, char delim) {
        std::string result;
        for (size_t i = 0; i < parts.size(); ++i) {
            if (i > 0) result += delim;
            result += parts[i];
        }
        return result;
    }

    static std::string toUpperJava(const std::string& s) {
        std::string result = s;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
        return result;
    }

    // Java saveFileName.split("\\.")[0]: text before first '.', or whole string if no '.'.
    static std::string baseName(const std::string& fileName) {
        size_t pos = fileName.find('.');
        return (pos == std::string::npos) ? fileName : fileName.substr(0, pos);
    }
};

} // namespace org_example