#include <cctype>
#include <map>
#include <string>
#include <vector>

class AutomaticGuitarSimulator {
public:
    explicit AutomaticGuitarSimulator(const std::string& text) : play_text(text) {}

    std::vector<std::map<std::string, std::string>> interpret(bool display_flag = false) const {
        if (is_blank(play_text)) {
            return {};
        }
        std::vector<std::map<std::string, std::string>> play_list;
        std::vector<std::string> play_segs = split(play_text, ' ');
        for (const std::string& play_seg : play_segs) {
            std::size_t pos = 0;
            while (pos < play_seg.size() &&
                   std::isalpha(static_cast<unsigned char>(play_seg[pos]))) {
                ++pos;
            }
            std::string play_chord = play_seg.substr(0, pos);
            std::string play_value = play_seg.substr(pos);
            play_list.push_back({{"Chord", play_chord}, {"Tune", play_value}});
            if (display_flag) {
                display(play_chord, play_value);
            }
        }
        return play_list;
    }

    std::string display(const std::string& key, const std::string& value) const {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }

private:
    std::string play_text;

    static bool is_blank(const std::string& s) {
        for (char c : s) {
            if (!std::isspace(static_cast<unsigned char>(c))) {
                return false;
            }
        }
        return true;
    }

    // Exact single-character split, matching Python's str.split(" ")
    // (empty segments preserved, no trimming).
    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string cur;
        for (char c : s) {
            if (c == delim) {
                parts.push_back(cur);
                cur.clear();
            } else {
                cur += c;
            }
        }
        parts.push_back(cur);
        return parts;
    }
};