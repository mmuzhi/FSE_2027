#include <string>
#include <vector>
#include <map>
#include <cctype>

class AutomaticGuitarSimulator {
public:
    // Initialize the score to be played
    explicit AutomaticGuitarSimulator(const std::string& text) : play_text(text) {}

    // Interpret the music score to be played.
    // Returns a list of dicts with keys "Chord" and "Tune".
    // If the input is empty or contains only whitespace, an empty list is returned.
    std::vector<std::map<std::string, std::string>> interpret(bool display = false) const {
        if (strip(play_text).empty()) {
            return {};
        } else {
            std::vector<std::map<std::string, std::string>> play_list;
            std::vector<std::string> play_segs = split(play_text, ' ');
            for (const std::string& play_seg : play_segs) {
                size_t pos = 0;
                for (char ele : play_seg) {
                    if (std::isalpha(static_cast<unsigned char>(ele))) {
                        pos += 1;
                        continue;
                    }
                    break;
                }
                std::string play_chord = play_seg.substr(0, pos);
                std::string play_value = play_seg.substr(pos);
                play_list.push_back({{"Chord", play_chord}, {"Tune", play_value}});
                if (display) {
                    // Return value discarded, mirroring the Python behavior.
                    (void)this->display(play_chord, play_value);
                }
            }
            return play_list;
        }
    }

    // Returns: "Normal Guitar Playing -- Chord: %s, Play Tune: %s"
    std::string display(const std::string& key, const std::string& value) const {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }

private:
    std::string play_text;

    // Equivalent of Python's str.strip() emptiness check (ASCII whitespace set).
    static std::string strip(const std::string& s) {
        const char* ws = " \t\n\r\v\f";
        size_t start = s.find_first_not_of(ws);
        if (start == std::string::npos) return "";
        size_t end = s.find_last_not_of(ws);
        return s.substr(start, end - start + 1);
    }

    // Equivalent of Python's str.split(" ") — exact single-space splitting,
    // preserving empty tokens (consecutive/trailing spaces).
    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> res;
        size_t start = 0;
        while (true) {
            size_t end = s.find(delim, start);
            if (end == std::string::npos) {
                res.push_back(s.substr(start));
                break;
            }
            res.push_back(s.substr(start, end - start));
            start = end + 1;
        }
        return res;
    }
};