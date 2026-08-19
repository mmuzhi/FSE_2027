#include <cstddef>
#include <string>
#include <vector>

namespace org {
namespace example {

class SplitSentence {
public:
    // Equivalent of regex "(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"
    // implemented manually (std::regex has no lookbehind support).
    std::vector<std::string> splitSentences(const std::string& sentencesString) const {
        std::vector<std::string> sentences;
        const std::size_t n = sentencesString.size();
        std::size_t lastEnd = 0;
        for (std::size_t i = 0; i < n; ++i) {
            if (!isJavaWhitespace(sentencesString[i])) continue;
            if (i == 0) continue;
            const char prev = sentencesString[i - 1];
            if (prev != '.' && prev != '?') continue; // (?<=\.|\?)
            // (?<!\w\.\w.): fails if chars [i-4..i-1] are \w '.' \w <any>.
            // The trailing regex '.' (any char but line terminators) always
            // matches prev, which is '.' or '?' here.
            if (i >= 4) {
                const char c4 = sentencesString[i - 4];
                const char c3 = sentencesString[i - 3];
                const char c2 = sentencesString[i - 2];
                if (isWordChar(c4) && c3 == '.' && isWordChar(c2)) continue;
            }
            // (?<![A-Z][a-z]\.)
            if (i >= 3) {
                const char c3 = sentencesString[i - 3];
                const char c2 = sentencesString[i - 2];
                if (c3 >= 'A' && c3 <= 'Z' && c2 >= 'a' && c2 <= 'z' && prev == '.') continue;
            }
            sentences.push_back(sentencesString.substr(lastEnd, i - lastEnd));
            lastEnd = i + 1;
        }
        if (lastEnd < n) {
            sentences.push_back(sentencesString.substr(lastEnd));
        }
        return sentences;
    }

    int countWords(const std::string& sentence) const {
        // replaceAll("[^a-zA-Z\\s]", "")
        std::string cleaned;
        for (char c : sentence) {
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || isJavaWhitespace(c)) {
                cleaned.push_back(c);
            }
        }
        // Emulates Java's cleaned.split("\\s+") semantics:
        // - pieces separated by runs of whitespace
        // - if no whitespace run occurs at all, result is {cleaned} (length 1)
        // - otherwise trailing empty pieces are dropped (result may be empty)
        std::vector<std::string> words;
        std::size_t start = 0;
        std::size_t i = 0;
        bool anyMatch = false;
        while (i < cleaned.size()) {
            if (!isJavaWhitespace(cleaned[i])) { ++i; continue; }
            anyMatch = true;
            words.push_back(cleaned.substr(start, i - start));
            while (i < cleaned.size() && isJavaWhitespace(cleaned[i])) ++i;
            start = i;
        }
        if (!anyMatch) {
            words.push_back(cleaned);
        } else {
            words.push_back(cleaned.substr(start));
            while (!words.empty() && words.back().empty()) words.pop_back();
        }
        return static_cast<int>(words.size());
    }

    int processTextFile(const std::string& sentencesString) const {
        const std::vector<std::string> sentences = splitSentences(sentencesString);
        int maxCount = 0;
        for (const std::string& sentence : sentences) {
            const int count = countWords(sentence);
            if (count > maxCount) {
                maxCount = count;
            }
        }
        return maxCount;
    }

private:
    // Java regex \s: [ \t\n\x0B\f\r]
    static bool isJavaWhitespace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\x0B' || c == '\f' || c == '\r';
    }
    // Java regex \w: [a-zA-Z0-9_]
    static bool isWordChar(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
               (c >= '0' && c <= '9') || c == '_';
    }
};

} // namespace example
} // namespace org