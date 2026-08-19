#include <regex>
#include <string>
#include <vector>

class RegexUtils {
public:
    // Check if the text matches the regular expression (anchored at the start,
    // equivalent to Python's re.match).
    bool match(const std::string& pattern, const std::string& text) {
        std::regex re(pattern);
        std::smatch m;
        // match_continuous: match must begin at the first character (like re.match),
        // not necessarily span the whole string (std::regex_match == re.fullmatch).
        return std::regex_search(text, m, re, std::regex_constants::match_continuous);
    }

    // Find all matching substrings and return a list of all matching substrings.
    std::vector<std::string> findall(const std::string& pattern, const std::string& text) {
        std::regex re(pattern);
        std::vector<std::string> result;
        auto it = std::sregex_iterator(text.begin(), text.end(), re);
        auto end = std::sregex_iterator();
        for (; it != end; ++it) {
            result.push_back(it->str());
        }
        return result;
    }

    // Split text based on regular expression patterns and return a list of substrings.
    // Preserves Python re.split behavior, including leading/trailing empty strings.
    std::vector<std::string> split(const std::string& pattern, const std::string& text) {
        std::regex re(pattern);
        std::vector<std::string> result;
        std::size_t last = 0;
        auto it = std::sregex_iterator(text.begin(), text.end(), re);
        auto end = std::sregex_iterator();
        for (; it != end; ++it) {
            result.push_back(text.substr(last, static_cast<std::size_t>(it->position()) - last));
            last = static_cast<std::size_t>(it->position()) + it->length();
        }
        result.push_back(text.substr(last));
        return result;
    }

    // Replace all substrings matched by the regular expression with the specified string.
    std::string sub(const std::string& pattern, const std::string& replacement, const std::string& text) {
        std::regex re(pattern);
        return std::regex_replace(text, re, replacement);
    }

    // Generate regular expression pattern that matches email addresses.
    std::string generate_email_pattern() {
        std::string pattern = "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b";
        return pattern;
    }

    // Generate regular expression pattern that matches phone numbers.
    std::string generate_phone_number_pattern() {
        std::string pattern = "\\b\\d{3}-\\d{3}-\\d{4}\\b";
        return pattern;
    }

    // Generate regular expression pattern that matches the middle characters of two sentences.
    std::string generate_split_sentences_pattern() {
        std::string pattern = "[.!?][\\s]{1,2}(?=[A-Z])";
        return pattern;
    }

    // Split the text into a list of sentences without punctuation except the last sentence.
    std::vector<std::string> split_sentences(const std::string& text) {
        std::string pattern = generate_split_sentences_pattern();
        return split(pattern, text);
    }

    // Verify if the phone number is valid.
    bool validate_phone_number(const std::string& phone_number) {
        std::string pattern = generate_phone_number_pattern();
        return match(pattern, phone_number);
    }

    // Extract all email addresses from the text.
    std::vector<std::string> extract_email(const std::string& text) {
        std::string pattern = generate_email_pattern();
        return findall(pattern, text);
    }
};