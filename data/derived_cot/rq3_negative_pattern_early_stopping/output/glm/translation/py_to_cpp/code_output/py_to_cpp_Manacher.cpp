#include <string>

class Manacher {
public:
    std::string input_string;

    Manacher(std::string input_string) : input_string(std::move(input_string)) {}

    int palindromic_length(int center, int diff, const std::string& string) {
        if (center - diff == -1 || center + diff == static_cast<int>(string.length())
                || string[center - diff] != string[center + diff]) {
            return 0;
        }
        return 1 + palindromic_length(center, diff + 1, string);
    }

    std::string palindromic_string() {
        int max_length = 0;
        int start = 0;

        std::string new_input_string;
        std::string output_string;

        if (input_string.empty()) {
            return output_string;
        }

        for (size_t i = 0; i + 1 < input_string.length(); ++i) {
            new_input_string += input_string[i];
            new_input_string += "|";
        }
        new_input_string += input_string.back();

        for (size_t i = 0; i < new_input_string.length(); ++i) {
            int length = palindromic_length(static_cast<int>(i), 1, new_input_string);

            if (max_length < length) {
                max_length = length;
                start = static_cast<int>(i);
            }
        }

        for (int i = start - max_length; i <= start + max_length; ++i) {
            if (new_input_string[i] != '|') {
                output_string += new_input_string[i];
            }
        }

        return output_string;
    }
};