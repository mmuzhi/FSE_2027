#include <string>
#include <vector>
#include <regex>

class RegexUtils {
public:
    bool match(const std::string& pattern, const std::string& text) {
        std::regex compiledPattern(pattern);
        return std::regex_match(text, compiledPattern);
    }

    std::vector<std::string> findall(const std::string& pattern, const std::string& text) {
        std::vector<std::string> matches;
        std::regex compiledPattern(pattern);
        
        auto begin = std::sregex_iterator(text.begin(), text.end(), compiledPattern);
        auto end = std::sregex_iterator();
        
        for (std::sregex_iterator i = begin; i != end; ++i) {
            matches.push_back(i->str());
        }
        
        return matches;
    }

    std::vector<std::string> split(const std::string& pattern, const std::string& text) {
        std::vector<std::string> splits;
        std::regex compiledPattern(pattern);
        
        // -1 as the submatch parameter returns the parts of the string that do not match the regex
        auto begin = std::sregex_token_iterator(text.begin(), text.end(), compiledPattern, -1);
        auto end = std::sregex_token_iterator();
        
        for (std::sregex_token_iterator i = begin; i != end; ++i) {
            splits.push_back(i->str());
        }
        
        return splits;
    }

    std::string sub(const std::string& pattern, const std::string& replacement, const std::string& text) {
        std::regex compiledPattern(pattern);
        return std::regex_replace(text, compiledPattern, replacement);
    }

    std::string generateEmailPattern() {
        return "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b";
    }

    std::string generatePhoneNumberPattern() {
        return "\\b\\d{3}-\\d{3}-\\d{4}\\b";
    }

    std::string generateSplitSentencesPattern() {
        return "[.!?][\\s]{1,2}(?=[A-Z])";
    }

    std::vector<std::string> splitSentences(const std::string& text) {
        std::string pattern = generateSplitSentencesPattern();
        return split(pattern, text);
    }

    bool validatePhoneNumber(const std::string& phoneNumber) {
        std::string pattern = generatePhoneNumberPattern();
        return match(pattern, phoneNumber);
    }

    std::vector<std::string> extractEmail(const std::string& text) {
        std::string pattern = generateEmailPattern();
        return findall(pattern, text);
    }
};