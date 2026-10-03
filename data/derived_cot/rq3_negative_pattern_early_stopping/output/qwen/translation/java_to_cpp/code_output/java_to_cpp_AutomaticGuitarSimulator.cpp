#include <vector>
#include <string>
#include <sstream>
#include <cctype>
#include <algorithm>
#include <iostream>

class AutomaticGuitarSimulator {
private:
    std::string playText;

    // Nested class for ChordTune
    struct ChordTune {
        std::string chord;
        std::string tune;

        ChordTune(const std::string& chord, const std::string& tune) : chord(chord), tune(tune) {}

        // Equality operator
        bool operator==(const ChordTune& other) const {
            return chord == other.chord && tune == other.tune;
        }

        // Hash code function
        int hashCode() const {
            // Using the same algorithm as Java: 
            //   result = chord.hashCode();
            //   result = 31 * result + tune.hashCode();
            // We'll compute the hash for the chord and tune strings.
            int result = 1;
            for (char c : chord) {
                result = 31 * result + static_cast<int>(c);
            }
            for (char c : tune) {
                result = 31 * result + static_cast<int>(c);
            }
            return result;
        }
    };

public:
    AutomaticGuitarSimulator(const std::string& text) : playText(text) {}

    std::vector<ChordTune> interpret(bool display) {
        // Check if playText is empty or contains only whitespace
        if (playText.empty() || playText.find_first_not_of(" \t\n\r") == std::string::npos) {
            return std::vector<ChordTune>();
        }

        std::vector<ChordTune> playList;
        std::istringstream iss(playText);
        std::string token;

        while (iss >> token) {
            // Count the number of consecutive letters at the beginning
            int pos = 0;
            for (char ele : token) {
                if (std::isalpha(static_cast<unsigned char>(ele))) {
                    pos++;
                } else {
                    break;
                }
            }

            if (pos == 0) {
                // No letters found, skip this token
                continue;
            }

            std::string playChord = token.substr(0, pos);
            std::string playValue = token.substr(pos);

            playList.push_back(ChordTune(playChord, playValue));

            if (display) {
                display(playChord, playValue);
            }
        }

        return playList;
    }

    std::string display(const std::string& key, const std::string& value) {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }
};