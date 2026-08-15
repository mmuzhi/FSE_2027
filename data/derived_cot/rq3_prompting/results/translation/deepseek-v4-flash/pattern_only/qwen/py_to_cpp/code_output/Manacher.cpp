#include <string>
#include <stdexcept>

class Manacher {
public:
    std::string input_string;

    Manacher(const std::string& input_string) : input_string(input_string) {}

    int palindromic_length(int center, int diff, const std::string& string) {
        if (center - diff == -1 || center + diff == (int)string.size() ||
            string[center - diff] != string[center + diff]) {
            return 0;
        }
        return 1 + palindromic_length(center, diff + 1, string);
    }

    std::string palindromic_string() {
        int max_length = 0;
        std::string new_input_string;
        std::string output_string;

        if (input_string.empty()) {
            throw std::out_of_range("IndexError: string index out of range");
        }

        for (int i = 0; i < (int)input_string.size() - 1; ++i) {
            new_input_string += input_string[i];
            new_input_string += '|';
        }
        new_input_string += input_string[(int)input_string.size() - 1];

        bool start_set = false;
        int start = 0;
        for (int i = 0; i < (int)new_input_string.size(); ++i) {
            int length = palindromic_length(i, 1, new_input_string);
            if (max_length < length) {
                max_length = length;
                start = i;
                start_set = true;
            }
        }

        if (!start_set) {
            throw std::runtime_error("NameError: name 'start' is not defined");
        }

        for (int i = start - max_length; i <= start + max_length; ++i) {
            if (new_input_string[i] != '|') {
                output_string += new_input_string[i];
            }
        }

        return output_string;
    }
};