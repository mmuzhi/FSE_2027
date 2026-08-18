#include <string>
#include <vector>

namespace org {
namespace example {

class SplitSentence {
public:
    // Equivalent of regex "(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s"
    // (std::regex has no lookbehind, so the assertion logic is expanded manually;
    //  Java's \w, \s and [A-Za-z] are all ASCII classes, so byte-wise checks match)
    std::vector<std::string> splitSentences(const std::string& sentencesString) const {
        std::vector<std::string> sentences;
        const int n = static_cast<int>(sentencesString.size());
        int lastEnd = 0;
        for (int p = 1; p < n; ++p) {
            if (!isJavaSpace(sentencesString[p])) continue;              // \s
            const char prev = sentencesString[p - 1];
            if (prev != '.' && prev != '?') continue;                    // (?<=\.|\?)
            // (?<!\w\.\w.)  -- trailing '.' in the lookbehind is regex "any char
            // except line terminator", which always holds since prev is '.' or '?'
            if (p >= 4 && isJavaWord(sentencesString[p - 4]) &&
                sentencesString[p - 3] == '.' &&
                isJavaWord(sentencesString[p - 2])) {
                continue;
            }
            // (?<![A-Z][a-z]\.)
            if (p >= 3 && isUpperAZ(sentencesString[p - 3]) &&
                isLowerAZ(sentencesString[p - 2]) &&
                prev == '.') {
                continue;
            }
            sentences.push_back(sentencesString.substr(lastEnd, p - lastEnd));
            lastEnd = p + 1;
        }
        if (lastEnd < n) {
            sentences.push_back(sentencesString.substr(lastEnd));
        }
        return sentences;
    }

    int countWords(const std::string& sentence) const {
        std::string cleaned;
        cleaned.reserve(sentence.size());
        for (char c : sentence) {
            if (isAsciiLetter(c) || isJavaSpace(c)) cleaned.push_back(c); // [^a-zA-Z\s] -> ""
        }
        return javaSplitWhitespaceCount(cleaned);
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
    // Java's default \s
    static bool isJavaSpace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\x0B' || c == '\f' || c == '\r';
    }
    // Java's default \w
    static bool isJavaWord(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') ||
               (c >= '0' && c <= '9') || c == '_';
    }
    static bool isUpperAZ(char c) { return c >= 'A' && c <= 'Z'; }
    static bool isLowerAZ(char c) { return c >= 'a' && c <= 'z'; }
    static bool isAsciiLetter(char c) { return isUpperAZ(c) || isLowerAZ(c); }

    // Equivalent of Java's cleaned.split("\\s+").length with limit 0:
    //  - a leading whitespace run yields a leading "" element,
    //  - trailing empty elements are dropped,
    //  - no match at all yields the whole string as one element (so "" -> 1).
    static int javaSplitWhitespaceCount(const std::string& cleaned) {
        const int n = static_cast<int>(cleaned.size());
        int matchCount = 0;
        int lastNonEmpty = -1;  // index of last non-empty segment
        int segStart = 0;
        int i = 0;
        while (i < n) {
            if (isJavaSpace(cleaned[i])) {
                if (i > segStart) lastNonEmpty = matchCount;  // segment before match
                ++matchCount;
                while (i < n && isJavaSpace(cleaned[i])) ++i;
                segStart = i;
            } else {
                ++i;
            }
        }
        if (n > segStart) lastNonEmpty = matchCount;          // final segment
        if (matchCount == 0) return 1;                        // Java: no match -> {input}
        return lastNonEmpty + 1;                              // trailing empties removed
    }
};

} // namespace example
} // namespace org