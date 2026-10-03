#include <regex>
#include <vector>
#include <string>

class RegexUtils {
public:
    static bool match(const std::string& pattern, const std::string& text) {
        std::regex compiledPattern(pattern);
        return std::regex_match(text, compiledPattern);
    }

    static std::vector<std::string> findall(const std::string& pattern, const std::string& text) {
        std::regex compiledPattern(pattern);
        std::sregex_iterator it(text.begin(), text.end(), compiledPattern);
        std::sregex_iterator end;
        std::vector<std::string> matches;
        while (it != end) {
            matches.push_back(it->str());
            ++it;
        }
        return matches;
    }

    static std::vector<std::string> split(const std::string& pattern, const std::string& text) {
        std::regex compiledPattern(pattern);
        std::sregex_token_iterator it(text.begin(), text.end(), compiledPattern, -1);
        std::sregex_token_iterator end;
        std::vector<std::string> splits;
        for (; it != end; ++it) {
            splits.push_back(*it);
        }
        return splits;
    }

    static std::string sub(const std::string& pattern, const std::string& replacement, const std::string& text) {
        std::regex compiledPattern(pattern);
        return std::regex_replace(text, compiledPattern, replacement);
    }

    static std::string generateEmailPattern() {
        return "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b";
    }

    static std::string generatePhoneNumberPattern() {
        return "\\b\\d{3}-\\d{3}-\\d{4}\\b";
    }

    static std::string generateSplitSentencesPattern() {
        return "[.!?][\\s]{1,2}(?=[A-Z])";
    }

    static std::vector<std::string> splitSentences(const std::string& text) {
        std::string pattern = generateSplitSentencesPattern();
        return split(pattern, text);
    }

    static bool validatePhoneNumber(const std::string& phoneNumber) {
        std::string pattern = generatePhoneNumberPattern();
        return match(pattern, phoneNumber);
    }

    static std::vector<std::string> extractEmail(const std::string& text) {
        std::string pattern = generateEmailPattern();
        return findall(pattern, text);
    }
};