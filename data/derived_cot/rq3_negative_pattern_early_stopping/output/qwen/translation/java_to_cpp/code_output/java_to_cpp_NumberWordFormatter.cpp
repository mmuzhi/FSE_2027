#include <vector>
#include <string>
#include <sstream>
#include <cctype>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <array>
#include <cctype>
#include <cstdlib>

class NumberWordFormatter {
private:
    static const std::vector<std::string> NUMBER;
    static const std::vector<std::string> NUMBER_TEEN;
    static const std::vector<std::string> NUMBER_TEN;
    static const std::vector<std::string> NUMBER_MORE;
    static const std::vector<std::string> NUMBER_SUFFIX;

    // Helper function to split a string by a delimiter
    std::vector<std::string> splitString(const std::string& s, char delimiter) {
        std::vector<std::string> parts;
        std::string part;
        std::istringstream tokenStream(s);
        while (std::getline(tokenStream, part, delimiter)) {
            parts.push_back(part);
        }
        return parts;
    }

    std::string transTwo(const std::string& s) {
        // Format the string to two digits, padding with zeros if necessary
        std::string formatted = s;
        if (formatted.length() == 1) {
            formatted = "0" + formatted;
        } else if (formatted.length() > 2) {
            // This should not happen because we are processing two-digit parts
            formatted = formatted.substr(formatted.length() - 2);
        }

        if (formatted[0] == '0') {
            // If the first digit is '0', then the second digit is the number
            if (formatted.length() == 2) {
                return NUMBER[std::stoi(formatted.substr(1))];
            } else {
                // This is a one-digit number (like "00") but we treat it as zero
                return NUMBER[0];
            }
        } else if (formatted[0] == '1') {
            // For numbers 10 to 19
            if (formatted.length() == 2) {
                return NUMBER_TEEN[std::stoi(formatted) - 10];
            } else {
                // This is a one-digit number starting with '1' (like "10") but we treat it as ten
                return NUMBER_TEEN[0];
            }
        } else if (formatted.length() == 2 && formatted[1] == '0') {
            // Like "20", "30", etc.
            return NUMBER_TEN[std::stoi(formatted.substr(0, 1)) - 1];
        } else {
            // Two-digit number with non-zero second digit
            return NUMBER_TEN[std::stoi(formatted.substr(0, 1)) - 1] + " " + NUMBER[std::stoi(formatted.substr(1))];
        }
    }

    std::string transThree(const std::string& s) {
        if (s.length() < 1 || s[0] == '0') {
            // If the string is empty or starts with '0', then we skip the hundreds part
            return transTwo(s.substr(1));
        } else if (s.length() == 3 && s[1] == '0' && s[2] == '0') {
            // Like "100", "200", etc.
            return NUMBER[std::stoi(s.substr(0, 1))] + " HUNDRED";
        } else {
            // Otherwise, we have a three-digit number with non-zero hundreds or non-zero tens/units
            return NUMBER[std::stoi(s.substr(0, 1))] + " HUNDRED AND " + transTwo(s.substr(1));
        }
    }

    std::string parseMore(int i) {
        if (i < NUMBER_MORE.size()) {
            return NUMBER_MORE[i];
        } else {
            // Return empty string if index is out of bounds
            return "";
        }
    }

public:
    NumberWordFormatter() {
        // Initialize the static members
        NUMBER = { "", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE" };
        NUMBER_TEEN = { "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN" };
        NUMBER_TEN = { "TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY" };
        NUMBER_MORE = { "", "THOUSAND", "MILLION", "BILLION" };
        NUMBER_SUFFIX = { "", "k", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e" };
    }

    std::string format(const std::string& x) {
        if (x.empty()) {
            return "";
        }
        return formatString(x);
    }

    std::string formatString(const std::string& x) {
        // Split the string by '.'
        std::vector<std::string> parts = splitString(x, '.');

        std::string lstr = parts[0];
        std::string rstr = parts.size() > 1 ? parts[1] : "";

        // Reverse the left string
        std::string lstrrev = std::string(lstr.rbegin(), lstr.rend());

        // Pad the reversed string with zeros to make its length a multiple of 3
        if (lstrrev.length() % 3 == 1) {
            lstrrev += "00";
        } else if (lstrrev.length() % 3 == 2) {
            lstrrev += "0";
        }

        std::string lm;
        for (int i = 0; i < lstrrev.length() / 3; i++) {
            std::string chunk = lstrrev.substr(3 * i, 3);
            std::reverse(chunk.begin(), chunk.end());
            if (chunk != "000") {
                lm = transThree(chunk) + " " + parseMore(i) + " " + lm;
            }
        }

        // If the left part is empty, we need to handle it
        if (lm.empty()) {
            return "ZERO ONLY";
        }

        std::string xs = !rstr.empty() ? "AND CENTS " + transTwo(rstr) + " " : "";
        return lm + xs + "ONLY";
    }
};

// Initialize static members outside the class
const std::vector<std::string> NumberWordFormatter::NUMBER = { "", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE" };
const std::vector<std::string> NumberWordFormatter::NUMBER_TEEN = { "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN", "EIGHTEEN", "NINETEEN" };
const std::vector<std::string> NumberWordFormatter::NUMBER_TEN = { "TEN", "TWENTY", "THIRTY", "FORTY", "FIFTY", "SIXTY", "SEVENTY", "EIGHTY", "NINETY" };
const std::vector<std::string> NumberWordFormatter::NUMBER_MORE = { "", "THOUSAND", "MILLION", "BILLION" };
const std::vector<std::string> NumberWordFormatter::NUMBER_SUFFIX = { "", "k", "", "m", "", "", "b", "", "", "t", "", "", "p", "", "", "e" };

// Example usage:
// int main() {
//     NumberWordFormatter formatter;
//     std::cout << formatter.format("123.45") << std::endl;
//     return 0;
// }