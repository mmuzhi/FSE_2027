#include <vector>
#include <string>
#include <cctype>

class SplitSentence {
private:
    static bool isWordChar(char c) {
        return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || (c >= '0' && c <= '9') || c == '_';
    }

    static bool isWhitespace(char c) {
        return c == ' ' || c == '\t' || c == '\n' || c == '\r' || c == '\f' || c == '\v';
    }

public:
    std::vector<std::string> splitSentences(const std::string& sentencesString) {
        std::vector<std::string> sentences;
        int lastEnd = 0;
        int len = static_cast<int>(sentencesString.length());

        for (int i = 1; i < len; ++i) {
            if (isWhitespace(sentencesString[i])) {
                char prev = sentencesString[i - 1];
                if (prev == '.' || prev == '?') {
                    bool neg1 = false;
                    if (i >= 4 && prev == '.') {
                        char c1 = sentencesString[i - 2];
                        char c2 = sentencesString[i - 3];
                        char c3 = sentencesString[i - 4];
                        if (isWordChar(c1) && c2 == '.' && isWordChar(c3)) {
                            neg1 = true;
                        }
                    }
                    bool neg2 = false;
                    if (i >= 3 && prev == '.') {
                        char c1 = sentencesString[i - 2];
                        char c2 = sentencesString[i - 3];
                        if (c1 >= 'a' && c1 <= 'z' && c2 >= 'A' && c2 <= 'Z') {
                            neg2 = true;
                        }
                    }
                    if (!neg1 && !neg2) {
                        sentences.push_back(sentencesString.substr(lastEnd, i - lastEnd));
                        lastEnd = i + 1;
                    }
                }
            }
        }
        if (lastEnd < len) {
            sentences.push_back(sentencesString.substr(lastEnd));
        }
        return sentences;
    }

    int countWords(const std::string& sentence) {
        std::string cleanedSentence;
        for (char c : sentence) {
            if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || isWhitespace(c)) {
                cleanedSentence += c;
            }
        }
        
        int count = 0;
        bool inWord = false;
        for (char c : cleanedSentence) {
            if (isWhitespace(c)) {
                inWord = false;
            } else {
                if (!inWord) {
                    count++;
                    inWord = true;
                }
            }
        }
        return count;
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
};