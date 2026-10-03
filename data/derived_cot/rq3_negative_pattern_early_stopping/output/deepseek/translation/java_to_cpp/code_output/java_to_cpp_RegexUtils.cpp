#include <string>
#include <vector>
#include <regex>

class RegexUtils {
public:
    bool match(const std::string& pattern, const std::string& text) const {
        std::regex compiledPattern(pattern);
        return std::regex_match(text, compiledPattern);
    }

    std::vector<std::string> findall(const std::string& pattern, const std::string& text) const {
        std::vector<std::string> matches;
        std::regex compiledPattern(pattern);
        auto words_begin = std::sregex_iterator(text.begin(), text.end(), compiledPattern);
        auto words_end = std::sregex_iterator();
        for (std::sregex_iterator i = words_begin; i != words_end; ++i) {
            matches.push_back(i->str());
        }
        return matches;
    }

    std::vector<std::string> split(const std::string& pattern, const std::string& text) const {
        std::regex compiledPattern(pattern);
        // -1 in Java split means keep trailing empty strings; regex_token_iterator with -1 does the same.
        std::sregex_token_iterator iter(text.begin(), text.end(), compiledPattern, -1);
        std::sregex_token_iterator end;
        std::vector<std::string> splits(iter, end);
        return splits;
    }

    std::string sub(const std::string& pattern, const std::string& replacement, const std::string& text) const {
        std::regex compiledPattern(pattern);
        return std::regex_replace(text, compiledPattern, replacement);
    }

    std::string generateEmailPattern() const {
        return R"(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)";
    }

    std::string generatePhoneNumberPattern() const {
        return R"(\b\d{3}-\d{3}-\d{4}\b)";
    }

    std::string generateSplitSentencesPattern() const {
        return R"([.!?][\s]{1,2}(?=[A-Z]))";
    }

    std::vector<std::string> splitSentences(const std::string& text) const {
        std::string pattern = generateSplitSentencesPattern();
        return split(pattern, text);
    }

    bool validatePhoneNumber(const std::string& phoneNumber) const {
        std::string pattern = generatePhoneNumberPattern();
        return match(pattern, phoneNumber);
    }

    std::vector<std::string> extractEmail(const std::string& text) const {
        std::string pattern = generateEmailPattern();
        return findall(pattern, text);
    }
};