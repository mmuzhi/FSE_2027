#include <string>
#include <vector>

class SplitSentence {
public:
    std::vector<std::string> splitSentences(const std::string& sentencesString) {
        std::vector<std::string> sentences;
        int n = static_cast<int>(sentencesString.size());
        int lastEnd = 0;

        for (int i = 0; i < n; ++i) {
            if (isSentenceBoundary(sentencesString, i)) {
                sentences.push_back(sentencesString.substr(lastEnd, i - lastEnd));
                lastEnd = i + 1;
            }
        }

        if (lastEnd < n) {
            sentences.push_back(sentencesString.substr(lastEnd));
        }

        return sentences;
    }

    int countWords(const std::string& sentence) {
        std::string cleaned;
        for (char c : sentence) {
            if (isAsciiLetter(c) || isJavaWhitespace(c)) {
                cleaned.push_back(c);
            }
        }
        return static_cast<int>(splitWhitespace(cleaned).size());
    }

    int processTextFile(const std::string& sentencesString) {
        std::vector<std::string> sentences = splitSentences(sentencesString);
        int maxCount = 0;

        for (const std::string& sentence : sentences) {
            int count = countWords(sentence);
            if (count > maxCount) {
                maxCount = count;
            }
        }

        return maxCount;
    }

private:
    static bool isAsciiLetter(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z');
    }

    static bool isUpperAscii(char c) {
        return c >= 'A' && c <= 'Z';
    }

    static bool isLowerAscii(char c) {
        return c >= 'a' && c <= 'z';
    }

    static bool isWordChar(char c) {
        return isAsciiLetter(c) || (c >= '0' && c <= '9') || c == '_';
    }

    static bool isJavaWhitespace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\v' || c == '\f' || c == '\r';
    }

    static bool isSentenceBoundary(const std::string& s, int i) {
        if (i <= 0 || i >= static_cast<int>(s.size())) {
            return false;
        }

        if (!isJavaWhitespace(s[i])) {
            return false;
        }

        char prev = s[i - 1];
        if (prev != '.' && prev != '?') {
            return false;
        }

        // Negative lookbehind (?<!\w\.\w.)
        if (i >= 4) {
            char a = s[i - 4];
            char b = s[i - 3];
            char c = s[i - 2];
            char d = s[i - 1];
            if (isWordChar(a) && b == '.' && isWordChar(c) && (d == '.' || d == '?')) {
                return false;
            }
        }

        // Negative lookbehind (?<![A-Z][a-z]\.)
        if (i >= 3) {
            char a = s[i - 3];
            char b = s[i - 2];
            char c = s[i - 1];
            if (isUpperAscii(a) && isLowerAscii(b) && c == '.') {
                return false;
            }
        }

        return true;
    }

    static std::vector<std::string> splitWhitespace(const std::string& s) {
        if (s.empty()) {
            return std::vector<std::string>{""};
        }

        std::vector<std::string> result;
        int n = static_cast<int>(s.size());
        int last = 0;
        int pos = 0;
        bool anyMatch = false;

        while (pos < n) {
            if (isJavaWhitespace(s[pos])) {
                anyMatch = true;
                result.push_back(s.substr(last, pos - last));

                while (pos < n && isJavaWhitespace(s[pos])) {
                    ++pos;
                }

                last = pos;
            } else {
                ++pos;
            }
        }

        if (last < n) {
            result.push_back(s.substr(last));
        } else if (anyMatch) {
            while (!result.empty() && result.back().empty()) {
                result.pop_back();
            }
        }

        return result;
    }
};