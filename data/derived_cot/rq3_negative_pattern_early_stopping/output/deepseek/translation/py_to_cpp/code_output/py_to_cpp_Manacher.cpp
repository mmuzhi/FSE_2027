#include <string>
#include <stdexcept>

class Manacher {
private:
    std::string input_string;

public:
    Manacher(const std::string& input_string) : input_string(input_string) {}

    int palindromic_length(int center, int diff, const std::string& str) const {
        int len = static_cast<int>(str.length());
        if (center - diff == -1 || center + diff == len ||
            str[center - diff] != str[center + diff]) {
            return 0;
        }
        return 1 + palindromic_length(center, diff + 1, str);
    }

    std::string palindromic_string() const {
        if (input_string.empty()) {
            throw std::out_of_range("IndexError: string index out of range");
        }

        std::string new_input_string;
        for (size_t i = 0; i < input_string.length() - 1; ++i) {
            new_input_string += input_string[i];
            new_input_string += '|';
        }
        new_input_string += input_string.back();

        int max_length = 0;
        int start = 0;
        int new_len = static_cast<int>(new_input_string.length());

        for (int i = 0; i < new_len; ++i) {
            int length = palindromic_length(i, 1, new_input_string);
            if (max_length < length) {
                max_length = length;
                start = i;
            }
        }

        std::string output_string;
        std::string substr = new_input_string.substr(start - max_length, 2 * max_length + 1);
        for (char ch : substr) {
            if (ch != '|') {
                output_string += ch;
            }
        }
        return output_string;
    }
};