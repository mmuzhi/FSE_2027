#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>

class Manacher {
public:
    explicit Manacher(const std::string& input_string) : input_string(input_string) {}

    int palindromic_length(int center, int diff, const std::string& string) {
        if (center - diff < 0 || center + diff >= string.length() || string[center - diff] != string[center + diff]) {
            return 0;
        }
        return 1 + palindromic_length(center, diff + 1, string);
    }

    std::string palindromic_string() {
        if (input_string.empty()) {
            throw std::runtime_error("Input string is empty");
        }

        std::string new_input_string;
        for (size_t i = 0; i < input_string.length() - 1; ++i) {
            new_input_string += input_string[i];
            new_input_string += '|';
        }
        new_input_string += input_string.back();

        int max_length = 0;
        int start_index = 0;

        for (int i = 0; i < new_input_string.length(); ++i) {
            int length = palindromic_length(i, 1, new_input_string);
            if (length > max_length) {
                max_length = length;
                start_index = i;
            }
        }

        std::string output_string;
        for (int i = start_index - max_length; i <= start_index + max_length; ++i) {
            if (i >= 0 && i < new_input_string.length() && new_input_string[i] != '|') {
                output_string += new_input_string[i];
            }
        }

        return output_string;
    }

private:
    std::string input_string;
};