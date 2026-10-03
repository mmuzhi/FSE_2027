#include <iostream>
#include <vector>
#include <string>
#include <sstream>

struct ChordTune {
    std::string chord;
    std::string tune;
};

class AutomaticGuitarSimulator {
private:
    std::string play_text;

    void display(const std::string& key, const std::string& value) {
        std::cout << "Normal Guitar Playing -- Chord: " << key << ", Play Tune: " << value << std::endl;
    }

    std::vector<ChordTune> processString(const std::string& text) {
        std::vector<ChordTune> result;
        std::istringstream iss(text);
        std::string token;

        while (iss >> token) {
            if (token.empty()) continue;

            size_t pos = 0;
            while (pos < token.size() && std::isalpha(token[pos])) {
                pos++;
            }

            std::string chord = token.substr(0, pos);
            std::string tune = token.substr(pos);

            result.push_back({chord, tune});
        }

        return result;
    }

public:
    AutomaticGuitarSimulator(const std::string& text) : play_text(text) {}

    std::vector<ChordTune> interpret(bool display = false) {
        if (play_text.empty() || play_text.find_first_not_of(" \t\n\r\f\v") == std::string::npos) {
            return {};
        }

        std::vector<ChordTune> play_list = processString(play_text);
        for (const auto& ct : play_list) {
            if (display) {
                display(ct.chord, ct.tune);
            }
        }

        return play_list;
    }
};