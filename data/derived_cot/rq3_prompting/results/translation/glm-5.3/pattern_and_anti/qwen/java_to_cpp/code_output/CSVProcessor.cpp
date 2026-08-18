#include <algorithm>
#include <cctype>
#include <fstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace org {
namespace example {

class CSVProcessor {
public:
    // Java: void readCSV(String, List<String>, List<List<String>>) throws IOException
    // Mutates title/data; throws on unreadable file (IOException equivalent).
    void readCSV(const std::string& fileName,
                 std::vector<std::string>& title,
                 std::vector<std::vector<std::string>>& data) {
        std::ifstream in(fileName);
        if (!in.is_open()) {
            throw std::runtime_error(fileName + " (No such file or directory)");
        }
        std::string line;
        if (std::getline(in, line)) {
            stripTrailingCR(line);
            std::vector<std::string> parts = javaSplit(line, ",");
            title.insert(title.end(), parts.begin(), parts.end());

            std::string lineData;
            while (std::getline(in, lineData)) {
                stripTrailingCR(lineData);
                data.push_back(javaSplit(lineData, ","));
            }
        }
    }

    // Java: int writeCSV(List<String>, List<List<String>>, String)
    // Returns 1 on success, 0 on I/O failure (IOException caught -> 0).
    int writeCSV(const std::vector<std::string>& title,
                 const std::vector<std::vector<std::string>>& data,
                 const std::string& fileName) {
        std::ofstream out(fileName);
        if (!out.is_open()) return 0;
        out << join(title) << "\n";
        for (const std::vector<std::string>& row : data) {
            out << join(row) << "\n";
        }
        out.close();
        return out.good() ? 1 : 0;
    }

    // Java overload: int writeCSV(List<List<String>>, String)
    int writeCSV(const std::vector<std::vector<std::string>>& data,
                 const std::string& fileName) {
        std::ofstream out(fileName);
        if (!out.is_open()) return 0;
        for (const std::vector<std::string>& row : data) {
            out << join(row) << "\n";
        }
        out.close();
        return out.good() ? 1 : 0;
    }

    // Java: int processCSVData(int, String) throws IOException
    int processCSVData(int N, const std::string& saveFileName) {
        std::vector<std::string> title;
        std::vector<std::vector<std::string>> data;
        readCSV(saveFileName, title, data);

        std::vector<std::string> columnData;
        for (const std::vector<std::string>& row : data) {
            // Java: N < row.size() (signed compare; negative N would throw on get)
            if (N < static_cast<long long>(row.size())) {
                columnData.push_back(toUpperCase(row.at(N)));
            }
        }

        std::vector<std::vector<std::string>> newData;
        newData.push_back(columnData);

        // Java: saveFileName.split("\\.")[0] — literal-dot split, take first part
        std::string base = javaSplit(saveFileName, ".").at(0);
        return writeCSV(title, newData, base + "_process.csv");
    }

private:
    // BufferedReader.readLine() strips '\n', "\r\n", and '\r'
    static void stripTrailingCR(std::string& s) {
        if (!s.empty() && s.back() == '\r') s.pop_back();
    }

    // Mimics Java String.split with limit 0: keeps leading empties,
    // drops trailing empties, "" -> {""}.
    static std::vector<std::string> javaSplit(const std::string& s, const std::string& delim) {
        std::vector<std::string> result;
        if (s.empty()) {
            result.push_back("");
            return result;
        }
        size_t start = 0;
        size_t pos;
        while ((pos = s.find(delim, start)) != std::string::npos) {
            result.push_back(s.substr(start, pos - start));
            start = pos + delim.size();
        }
        result.push_back(s.substr(start));
        while (!result.empty() && result.back().empty()) {
            result.pop_back();
        }
        return result;
    }

    // Mimics String.join(",", parts)
    static std::string join(const std::vector<std::string>& parts) {
        std::string result;
        for (size_t i = 0; i < parts.size(); ++i) {
            if (i > 0) result += ",";
            result += parts[i];
        }
        return result;
    }

    // Mimics String.toUpperCase() (ASCII behavior)
    static std::string toUpperCase(const std::string& s) {
        std::string result = s;
        std::transform(result.begin(), result.end(), result.begin(),
                       [](unsigned char c) { return static_cast<char>(std::toupper(c)); });
        return result;
    }
};

} // namespace example
} // namespace org