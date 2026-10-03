#include <string>
#include <vector>
#include <sstream>
#include <cctype>

class AutomaticGuitarSimulator {
private:
    std::string play_text;

public:
    AutomaticGuitarSimulator(const std::string& text) : play_text(text) {}

    struct ChordTune {
        std::string Chord;
        std::string Tune;
    };

    std::vector<ChordTune> interpret(bool display = false) {
        std::vector<ChordTune> result;
        std::string trimmed = play_text;
        // trim whitespace (leading/trailing)
        size_t start = trimmed.find_first_not_of(" \t\n\r\f\v");
        if (start == std::string::npos) {
            return result;
        }
        size_t end = trimmed.find_last_not_of(" \t\n\r\f\v");
        trimmed = trimmed.substr(start, end - start + 1);

        std::istringstream iss(trimmed);
        std::string token;
        while (iss >> token) {
            size_t pos = 0;
            while (pos < token.size() && std::isalpha(static_cast<unsigned char>(token[pos]))) {
                ++pos;
            }
            std::string chord = token.substr(0, pos);
            std::string tune = token.substr(pos);
            result.push_back({chord, tune});
            if (display) {
                this->display(chord, tune);
            }
        }
        return result;
    }

    std::string display(const std::string& key, const std::string& value) {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }
};