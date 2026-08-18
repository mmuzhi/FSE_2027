#include <string>
#include <vector>
#include <sstream>
#include <iterator>
#include <algorithm>

class NLPDataProcessor {
public:
    // Construct a stop word list including 'a', 'an', 'the'.
    std::vector<std::string> construct_stop_word_list() const {
        std::vector<std::string> stop_word_list;
        stop_word_list.push_back("a");
        stop_word_list.push_back("an");
        stop_word_list.push_back("the");
        return stop_word_list;
    }

    // Remove all the stop words from the list of strings.
    // Replicates Python's mutation-during-iteration semantics exactly:
    // the loop index keeps advancing while list.remove() erases the FIRST
    // occurrence of the matched word, so consecutive stop words may skip.
    std::vector<std::vector<std::string> > remove_stop_words(
            const std::vector<std::string>& string_list,
            const std::vector<std::string>& stop_word_list) const {
        std::vector<std::vector<std::string> > answer;
        answer.reserve(string_list.size());

        for (std::vector<std::string>::const_iterator s_it = string_list.begin();
             s_it != string_list.end(); ++s_it) {
            std::vector<std::string> string_split = split(*s_it);

            for (size_t i = 0; i < string_split.size(); ++i) {
                std::string word = string_split[i];  // copy before potential erase
                if (std::find(stop_word_list.begin(), stop_word_list.end(), word)
                        != stop_word_list.end()) {
                    // list.remove(word): erase first occurrence
                    std::vector<std::string>::iterator pos =
                        std::find(string_split.begin(), string_split.end(), word);
                    if (pos != string_split.end()) {
                        string_split.erase(pos);
                    }
                }
            }
            answer.push_back(string_split);
        }
        return answer;
    }

    // Construct a stop word list and remove all stop words from the strings.
    std::vector<std::vector<std::string> > process(
            const std::vector<std::string>& string_list) const {
        std::vector<std::string> stop_word_list = construct_stop_word_list();
        return remove_stop_words(string_list, stop_word_list);
    }

private:
    // Equivalent of Python str.split(): split on runs of whitespace,
    // ignoring leading/trailing whitespace; empty input -> empty list.
    static std::vector<std::string> split(const std::string& s) {
        std::vector<std::string> tokens;
        std::istringstream iss(s);
        std::string word;
        while (iss >> word) {
            tokens.push_back(word);
        }
        return tokens;
    }
};