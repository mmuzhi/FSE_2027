#include <string>
#include <vector>
#include <optional>
#include <cctype>

class AutomaticGuitarSimulator {
private:
    std::string playText;

public:
    AutomaticGuitarSimulator(const std::string& text) : playText(text) {}

    struct ChordTune {
        std::string chord;
        std::string tune;

        ChordTune(const std::string& chord, const std::string& tune) : chord(chord), tune(tune) {}
    };

    std::optional<std::vector<ChordTune>> interpret(bool display) {
        if (playText.empty() || playText.find_first_not_of(' ') == std::string::npos) {
            return std::nullopt;
        }

        std::vector<ChordTune> playList;
        std::istringstream iss(playText);
        std::string playSeg;
        while (iss >> playSeg) {
            int pos = 0;
            for (char ele : playSeg) {
                if (std::isalpha(static_cast<unsigned char>(ele))) {
                    ++pos;
                } else {
                    break;
                }
            }
            std::string playChord = playSeg.substr(0, pos);
            std::string playValue = playSeg.substr(pos);
            playList.emplace_back(playChord, playValue);
            if (display) {
                display(playChord, playValue);
            }
        }
        return playList;
    }

    std::string display(const std::string& key, const std::string& value) const {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }

    // Needed for std::istringstream
    #include <sstream>
};