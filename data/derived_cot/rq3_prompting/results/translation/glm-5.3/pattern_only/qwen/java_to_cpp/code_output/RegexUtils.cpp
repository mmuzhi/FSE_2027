#include <regex>
#include <string>
#include <vector>

class RegexUtils {
public:
    bool match(const std::string& pattern, const std::string& text) {
        std::regex compiledPattern(pattern);
        return std::regex_match(text, compiledPattern);
    }

    std::vector<std::string> findall(const std::string& pattern, const std::string& text) {
        std::vector<std::string> matches;
        std::regex compiledPattern(pattern);
        auto end = std::sregex_iterator();
        for (auto it = std::sregex_iterator(text.begin(), text.end(), compiledPattern);
             it != end; ++it) {
            matches.push_back(it->str());
        }
        return matches;
    }

    // Equivalent of Java Pattern.split(text, -1): trailing empty strings kept,
    // and a zero-width match at position 0 does not yield a leading "".
    std::vector<std::string> split(const std::string& pattern, const std::string& text) {
        std::regex compiledPattern(pattern);
        std::vector<std::string> splits;
        std::size_t index = 0;
        for (auto it = std::sregex_iterator(text.begin(), text.end(), compiledPattern);
             it != std::sregex_iterator(); ++it) {
            const std::smatch& m = *it;
            if (index == 0 && m.position() == 0 && m.length() == 0) {
                continue; // Java: no empty leading substring for zero-width match at start
            }
            std::size_t start = static_cast<std::size_t>(m.position());
            std::size_t len = static_cast<std::size_t>(m.length());
            splits.push_back(text.substr(index, start - index));
            index = start + len;
        }
        if (index == 0) {
            // Java: if no match was found, return the input itself
            return {text};
        }
        splits.push_back(text.substr(index));
        return splits;
    }

    std::string sub(const std::string& pattern, const std::string& replacement,
                    const std::string& text) {
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