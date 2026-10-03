#include <string>
#include <vector>
#include <regex>
#include <cctype>

class SplitSentence {
public:
    std::vector<std::string> splitSentences(const std::string& sentencesString) {
        std::vector<std::string> sentences;
        size_t lastEnd = 0;
        for (size_t w = 0; w < sentencesString.size(); ++w) {
            // Check if this position is a whitespace preceded by '.' or '?'
            if (!std::isspace(static_cast<unsigned char>(sentencesString[w])))
                continue;
            if (w == 0) continue;
            char prev = sentencesString[w - 1];
            if (prev != '.' && prev != '?')
                continue;
            
            // Negative lookbehind 1: (?<!\w\.\w.)
            bool neg1 = false;
            if (w >= 4) {
                if (sentencesString[w-1] == '.' &&
                    std::isalnum(static_cast<unsigned char>(sentencesString[w-4])) &&
                    sentencesString[w-3] == '.' &&
                    std::isalnum(static_cast<unsigned char>(sentencesString[w-2])) &&
                    std::isalnum(static_cast<unsigned char>(sentencesString[w-1]))) // Actually pattern ends with ., which is already checked
                {
                    // The full pattern: \w\.\w.  -> last char (w-1) is '.' and first three are \w, '.', \w
                    // But the check above uses w-1 == '.', w-4 is word, w-3 is '.', w-2 is word.
                    // The final '.' in pattern is w-1.
                    neg1 = true;
                }
            }
            
            // Negative lookbehind 2: (?<![A-Z][a-z]\.)
            bool neg2 = false;
            if (w >= 3) {
                if (sentencesString[w-1] == '.' &&
                    std::isupper(static_cast<unsigned char>(sentencesString[w-3])) &&
                    std::islower(static_cast<unsigned char>(sentencesString[w-2])))
                {
                    neg2 = true;
                }
            }
            
            if (!neg1 && !neg2) {
                // it's a sentence boundary
                sentences.push_back(sentencesString.substr(lastEnd, w - lastEnd - 1)); // from lastEnd to before the period/question mark? Wait: we want up to w-1 inclusive.
                // Actually w-1 is the period/question mark. So substr(lastEnd, (w - lastEnd - 1)) gives characters from lastEnd inclusive, length = w-lastEnd, but we want exclude the whitespace, include the punctuation? Let's check: Example "Hello world. Next." 
                // positions: H0 e1 l2 l3 o4 ' '5 w6 o7 r8 l9 d10 .11 ' '12 N13 ... 
                // For boundary at w=12 (space after period). lastEnd=0. w-lastEnd-1 = 12-0-1=11 -> substr(0,11) gives "Hello world." which is correct (includes period, excludes space). Then lastEnd = w+1 = 13.
                // For second sentence, lastEnd=13, w? Next boundary? until end, add substr(lastEnd). That works.
                sentences.push_back(sentencesString.substr(lastEnd, w - lastEnd - 1));
                lastEnd = w + 1;
            }
        }
        if (lastEnd < sentencesString.size()) {
            sentences.push_back(sentencesString.substr(lastEnd));
        }
        return sentences;
    }

    int countWords(const std::string& sentence) {
        // Remove all non-alphabetic characters (except whitespace)
        std::string cleaned;
        for (char ch : sentence) {
            if (std::isalpha(static_cast<unsigned char>(ch)) || std::isspace(static_cast<unsigned char>(ch)))
                cleaned.push_back(ch);
        }
        // Split on whitespace
        std::regex ws_re("\\s+");
        std::sregex_token_iterator it(cleaned.begin(), cleaned.end(), ws_re, -1);
        std::sregex_token_iterator end;
        int count = 0;
        while (it != end) {
            if (!it->str().empty()) count++;
            ++it;
        }
        return count;
    }

    int processTextFile(const std::string& sentencesString) {
        std::vector<std::string> sentences = splitSentences(sentencesString);
        int maxCount = 0;
        for (const auto& sentence : sentences) {
            int count = countWords(sentence);
            if (count > maxCount) maxCount = count;
        }
        return maxCount;
    }
};