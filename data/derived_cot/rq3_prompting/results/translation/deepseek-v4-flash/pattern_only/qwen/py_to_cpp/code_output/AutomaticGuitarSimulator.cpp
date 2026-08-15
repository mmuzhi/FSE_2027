#include <string>
#include <vector>
#include <cctype>

struct PlayItem {
    std::string Chord;
    std::string Tune;
};

class AutomaticGuitarSimulator {
public:
    AutomaticGuitarSimulator(const std::string& text) : play_text(text) {}

    std::vector<PlayItem> interpret(bool display = false) {
        if (is_blank(play_text)) {
            return {};
        }

        std::vector<PlayItem> play_list;
        size_t start = 0;
        while (start <= play_text.size()) {
            size_t pos = play_text.find(' ', start);
            std::string play_seg;
            if (pos == std::string::npos) {
                play_seg = play_text.substr(start);
                start = play_text.size() + 1;
            } else {
                play_seg = play_text.substr(start, pos - start);
                start = pos + 1;
            }

            size_t p = 0;
            while (p < play_seg.size() && is_alpha(play_seg[p])) {
                ++p;
            }
            std::string play_chord = play_seg.substr(0, p);
            std::string play_value = play_seg.substr(p);

            play_list.push_back({play_chord, play_value});
            if (display) {
                this->display(play_chord, play_value);
            }
        }
        return play_list;
    }

    std::string display(const std::string& key, const std::string& value) {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }

private:
    std::string play_text;

    static bool is_alpha(char c) {
        return std::isalpha(static_cast<unsigned char>(c)) != 0;
    }

    static bool is_blank(const std::string& s) {
        for (char c : s) {
            if (std::isspace(static_cast<unsigned char>(c)) == 0) {
                return false;
            }
        }
        return true;
    }
};