#include <regex>
#include <string>
#include <vector>

/**
 * The class provides to match, find all occurrences, split, and substitute
 * text using regular expressions. It also includes predefined patterns,
 * validating phone numbers and extracting email addresses.
 *
 * Uses std::regex with ECMAScript syntax, which is compatible with the
 * Python regex patterns used here (\b, \d, \s, lookahead (?=...), etc.).
 * Invalid patterns throw std::regex_error, analogous to Python's re.error.
 */
class RegexUtils {
public:
    // Equivalent of Python's re.match: anchored at the start of the text,
    // but NOT required to consume the whole text (std::regex_match would).
    bool match(const std::string& pattern, const std::string& text) const {
        std::regex re(pattern);
        std::smatch m;
        if (std::regex_search(text, m, re) && m.position() == 0)
            return true;
        return false;
    }

    // Equivalent of Python's re.findall: returns full match strings;
    // if the pattern has exactly one capture group, that group is returned.
    std::vector<std::string> findall(const std::string& pattern, const std::string& text) const {
        std::regex re(pattern);
        std::vector<std::string> result;
        auto end = std::sregex_iterator();
        for (auto it = std::sregex_iterator(text.begin(), text.end(), re); it != end; ++it) {
            if (re.mark_count() == 1)
                result.push_back(it->str(1));
            else
                result.push_back(it->str(0));
        }
        return result;
    }

    // Equivalent of Python's re.split: keeps empty leading/trailing pieces.
    std::vector<std::string> split(const std::string& pattern, const std::string& text) const {
        std::regex re(pattern);
        std::vector<std::string> result;
        std::size_t last = 0;
        auto end = std::sregex_iterator();
        for (auto it = std::sregex_iterator(text.begin(), text.end(), re); it != end; ++it) {
            std::size_t pos = static_cast<std::size_t>(it->position());
            std::size_t len = static_cast<std::size_t>(it->length());
            result.push_back(text.substr(last, pos - last));
            last = pos + len;
        }
        result.push_back(text.substr(last));
        return result;
    }

    // Equivalent of Python's re.sub for the common replacement forms:
    // '$' is literal (escaped to '$$'), '\1'..'9' and '\g<1>'..'9' become
    // backreferences, '\\' becomes a single backslash; other chars pass through.
    std::string sub(const std::string& pattern, const std::string& replacement,
                    const std::string& text) const {
        std::regex re(pattern);
        return std::regex_replace(text, re, translate_replacement(replacement));
    }

    // Generate regular expression patterns that match email addresses
    std::string generate_email_pattern() const {
        return R"(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)";
    }

    // Generate regular expression patterns that match phone numbers
    std::string generate_phone_number_pattern() const {
        return R"(\b\d{3}-\d{3}-\d{4}\b)";
    }

    // Generate regular expression patterns that match the middle characters
    // of two sentences
    std::string generate_split_sentences_pattern() const {
        return R"([.!?][\s]{1,2}(?=[A-Z]))";
    }

    // Split the text into a list of sentences without Punctuation except the
    // last sentence
    std::vector<std::string> split_sentences(const std::string& text) const {
        return split(generate_split_sentences_pattern(), text);
    }

    // Verify if the phone number is valid
    bool validate_phone_number(const std::string& phone_number) const {
        return match(generate_phone_number_pattern(), phone_number);
    }

    // Extract all email addresses from the text
    std::vector<std::string> extract_email(const std::string& text) const {
        return findall(generate_email_pattern(), text);
    }

private:
    // Python replacement syntax -> std::regex_replace format syntax
    static std::string translate_replacement(const std::string& repl) {
        std::string out;
        out.reserve(repl.size());
        for (std::size_t i = 0; i < repl.size(); ++i) {
            char c = repl[i];
            if (c == '$') {
                out += "$$";                       // '$' is literal in Python
            } else if (c == '\\' && i + 1 < repl.size()) {
                char n = repl[++i];
                if (n >= '1' && n <= '9') {        // \1 -> $1
                    out += '$';
                    out += n;
                } else if (n == 'g' && i + 3 < repl.size() && repl[i + 1] == '<' &&
                           repl[i + 2] >= '1' && repl[i + 2] <= '9' && repl[i + 3] == '>') {
                    out += '$';                    // \g<1> -> $1
                    out += repl[i + 2];
                    i += 3;
                } else if (n == '\\') {            // \\ -> single backslash
                    out += '\\';
                } else if (n == 'n') {
                    out += '\n';
                } else if (n == 't') {
                    out += '\t';
                } else if (n == 'r') {
                    out += '\r';
                } else {
                    out += n;
                }
            } else {
                out += c;
            }
        }
        return out;
    }
};