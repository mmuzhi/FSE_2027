#ifndef AUTOMATIC_GUITAR_SIMULATOR_H
#define AUTOMATIC_GUITAR_SIMULATOR_H

#include <string>
#include <vector>
#include <optional>
#include <sstream>
#include <cctype>
#include <cstdint>

class AutomaticGuitarSimulator {
public:
    class ChordTune {
    private:
        std::string chord;
        std::string tune;

    public:
        ChordTune(const std::string& chord, const std::string& tune)
            : chord(chord), tune(tune) {}

        const std::string& getChord() const {
            return chord;
        }

        const std::string& getTune() const {
            return tune;
        }

        bool equals(const ChordTune& that) const {
            return chord == that.chord && tune == that.tune;
        }

        bool operator==(const ChordTune& that) const {
            return equals(that);
        }

        int32_t hashCode() const {
            int32_t result = javaStringHashCode(chord);
            result = 31 * result + javaStringHashCode(tune);
            return result;
        }

    private:
        static int32_t javaStringHashCode(const std::string& s) {
            uint32_t h = 0;
            for (unsigned char c : s) {
                h = 31 * h + static_cast<uint32_t>(c);
            }
            return static_cast<int32_t>(h);
        }
    };

private:
    std::string playText;

    static std::string trim(const std::string& s) {
        size_t start = s.find_first_not_of(" \t\n\r\f\v");
        if (start == std::string::npos) return "";
        size_t end = s.find_last_not_of(" \t\n\r\f\v");
        return s.substr(start, end - start + 1);
    }

    static std::vector<std::string> splitBySpace(const std::string& s) {
        std::vector<std::string> result;
        std::string current;
        for (char c : s) {
            if (c == ' ') {
                result.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        result.push_back(current);
        return result;
    }

public:
    AutomaticGuitarSimulator(const std::string& text) : playText(text) {}

    std::optional<std::vector<ChordTune>> interpret(bool display) {
        if (trim(playText).empty()) {
            return std::nullopt;
        }

        std::vector<ChordTune> playList;
        std::vector<std::string> playSegs = splitBySpace(playText);
        for (const std::string& playSeg : playSegs) {
            if (trim(playSeg).empty()) {
                continue;
            }
            int pos = 0;
            for (char ele : playSeg) {
                if (std::isalpha(static_cast<unsigned char>(ele))) {
                    pos++;
                    continue;
                }
                break;
            }
            std::string playChord = playSeg.substr(0, pos);
            std::string playValue = playSeg.substr(pos);
            playList.emplace_back(playChord, playValue);
            if (display) {
                this->display(playChord, playValue);
            }
        }
        return playList;
    }

    std::string display(const std::string& key, const std::string& value) {
        std::ostringstream oss;
        oss << "Normal Guitar Playing -- Chord: " << key << ", Play Tune: " << value;
        return oss.str();
    }
};

#endif