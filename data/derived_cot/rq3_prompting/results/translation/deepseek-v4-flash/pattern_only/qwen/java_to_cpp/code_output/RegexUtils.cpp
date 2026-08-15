#include <regex>
#include <string>
#include <vector>
#include <stdexcept>

class RegexUtils {
public:
    virtual ~RegexUtils() = default;

    virtual bool match(const std::string& pattern, const std::string& text) {
        if (pattern == generateSplitSentencesPattern()) {
            return false;
        }
        std::regex re(pattern);
        return std::regex_match(text, re);
    }

    virtual std::vector<std::string> findall(const std::string& pattern, const std::string& text) {
        if (pattern == generateSplitSentencesPattern()) {
            return findallSplitSentences(text);
        }
        std::vector<std::string> matches;
        std::regex re(pattern);
        auto begin = std::sregex_iterator(text.begin(), text.end(), re);
        auto end = std::sregex_iterator();
        for (auto it = begin; it != end; ++it) {
            matches.push_back(it->str());
        }
        return matches;
    }

    virtual std::vector<std::string> split(const std::string& pattern, const std::string& text) {
        if (pattern == generateSplitSentencesPattern()) {
            return splitSentencesImpl(text);
        }
        std::vector<std::string> splits;
        std::regex re(pattern);
        std::sregex_token_iterator it(text.begin(), text.end(), re, -1);
        std::sregex_token_iterator end;
        for (; it != end; ++it) {
            splits.push_back(*it);
        }
        return splits;
    }

    virtual std::string sub(const std::string& pattern, const std::string& replacement, const std::string& text) {
        if (pattern == generateSplitSentencesPattern()) {
            return subSplitSentences(replacement, text);
        }
        std::regex re(pattern);
        return std::regex_replace(text, re, replacement);
    }

    virtual std::string generateEmailPattern() const {
        return R"(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)";
    }

    virtual std::string generatePhoneNumberPattern() const {
        return R"(\b\d{3}-\d{3}-\d{4}\b)";
    }

    virtual std::string generateSplitSentencesPattern() const {
        return R"([.!?][\s]{1,2}(?=[A-Z]))";
    }

    virtual std::vector<std::string> splitSentences(const std::string& text) {
        return split(generateSplitSentencesPattern(), text);
    }

    virtual bool validatePhoneNumber(const std::string& phoneNumber) {
        return match(generatePhoneNumberPattern(), phoneNumber);
    }

    virtual std::vector<std::string> extractEmail(const std::string& text) {
        return findall(generateEmailPattern(), text);
    }

private:
    static bool isWhitespace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
    }

    static bool isUpper(char c) {
        return c >= 'A' && c <= 'Z';
    }

    static bool isDigit(char c) {
        return c >= '0' && c <= '9';
    }

    static bool matchSplitSentencesDelimiter(const std::string& text, size_t i, size_t& end) {
        if (i >= text.size()) return false;
        char c = text[i];
        if (c != '.' && c != '!' && c != '?') return false;

        size_t j = i + 1;
        int wsCount = 0;
        while (j < text.size() && wsCount < 2 && isWhitespace(text[j])) {
            ++wsCount;
            ++j;
        }

        if (wsCount > 0 && j < text.size() && isUpper(text[j])) {
            end = j;
            return true;
        }
        return false;
    }

    static std::vector<std::string> splitSentencesImpl(const std::string& text) {
        std::vector<std::string> result;
        size_t start = 0;
        size_t i = 0;

        while (i < text.size()) {
            size_t end;
            if (matchSplitSentencesDelimiter(text, i, end)) {
                result.push_back(text.substr(start, i - start));
                start = end;
                i = end;
                continue;
            }
            ++i;
        }

        result.push_back(text.substr(start));
        return result;
    }

    static std::vector<std::string> findallSplitSentences(const std::string& text) {
        std::vector<std::string> matches;
        size_t i = 0;

        while (i < text.size()) {
            size_t end;
            if (matchSplitSentencesDelimiter(text, i, end)) {
                matches.push_back(text.substr(i, end - i));
                i = end;
                continue;
            }
            ++i;
        }

        return matches;
    }

    static std::string subSplitSentences(const std::string& replacement, const std::string& text) {
        std::string result;
        size_t start = 0;
        size_t i = 0;

        while (i < text.size()) {
            size_t end;
            if (matchSplitSentencesDelimiter(text, i, end)) {
                result.append(text, start, i - start);
                std::string delimiter = text.substr(i, end - i);
                result += processReplacementNoGroups(replacement, delimiter);
                start = end;
                i = end;
                continue;
            }
            ++i;
        }

        result.append(text, start, std::string::npos);
        return result;
    }

    static std::string processReplacementNoGroups(const std::string& replacement, const std::string& matched) {
        std::string out;

        for (size_t i = 0; i < replacement.size(); ++i) {
            char c = replacement[i];

            if (c == '\\') {
                if (i + 1 < replacement.size()) {
                    out += replacement[i + 1];
                    ++i;
                } else {
                    throw std::invalid_argument("character to be escaped is missing");
                }
            } else if (c == '$') {
                if (i + 1 < replacement.size() && isDigit(replacement[i + 1])) {
                    size_t num = 0;
                    size_t j = i + 1;
                    while (j < replacement.size() && isDigit(replacement[j])) {
                        num = num * 10 + (replacement[j] - '0');
                        ++j;
                    }

                    if (num == 0) {
                        out += matched;
                    } else {
                        throw std::invalid_argument("No group " + std::to_string(num));
                    }

                    i = j - 1;
                } else {
                    out += '$';
                }
            } else {
                out += c;
            }
        }

        return out;
    }
};