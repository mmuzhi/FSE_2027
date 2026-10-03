#include <string>
#include <vector>
#include <unordered_map>
#include <cctype>

class AutomaticGuitarSimulator {
public:
    AutomaticGuitarSimulator(const std::string& text) : play_text(text) {}

    std::vector<std::unordered_map<std::string, std::string>> interpret(bool display = false) {
        // Check if play_text is empty or contains only whitespace
        bool all_whitespace = true;
        for (char c : play_text) {
            if (!std::isspace(static_cast<unsigned char>(c))) {
                all_whitespace = false;
                break;
            }
        }
        if (all_whitespace) {
            return {};
        }

        // Split by single space (matching Python's split(" "))
        std::vector<std::string> play_segs;
        std::string current;
        for (size_t i = 0; i < play_text.size(); ++i) {
            if (play_text[i] == ' ') {
                play_segs.push_back(current);
                current.clear();
            } else {
                current += play_text[i];
            }
        }
        play_segs.push_back(current);

        std::vector<std::unordered_map<std::string, std::string>> play_list;

        for (const auto& play_seg : play_segs) {
            int pos = 0;
            for (char ele : play_seg) {
                if (std::isalpha(static_cast<unsigned char>(ele))) {
                    pos++;
                    continue;
                }
                break;
            }
            std::string play_chord = play_seg.substr(0, pos);
            std::string play_value = play_seg.substr(pos);

            std::unordered_map<std::string, std::string> entry;
            entry["Chord"] = play_chord;
            entry["Tune"] = play_value;
            play_list.push_back(entry);

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
};