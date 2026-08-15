#include <optional>
#include <string>
#include <vector>
#include <sstream>
#include <cstdint>
#include <cstddef>
#include <functional>
#include <utility>

class AutomaticGuitarSimulator {
public:
    class ChordTune {
    private:
        std::string chord;
        std::string tune;

        static int javaStringHashCode(const std::string& s) {
            uint32_t h = 0;
            for (unsigned char c : s) {
                h = 31 * h + static_cast<uint32_t>(c);
            }
            return static_cast<int32_t>(h);
        }

    public:
        explicit ChordTune(std::string chord, std::string tune)
            : chord(std::move(chord)), tune(std::move(tune)) {}

        const std::string& getChord() const { return chord; }
        const std::string& getTune() const { return tune; }

        bool operator==(const ChordTune& other) const {
            return chord == other.chord && tune == other.tune;
        }

        bool operator!=(const ChordTune& other) const {
            return !(*this == other);
        }

        int hashCode() const {
            uint32_t h = static_cast<uint32_t>(javaStringHashCode(chord));
            h = 31 * h + static_cast<uint32_t>(javaStringHashCode(tune));
            return static_cast<int32_t>(h);
        }
    };

private:
    std::optional<std::string> playText;

    static bool isTrimChar(char c) {
        return static_cast<unsigned char>(c) <= 0x20;
    }

    static std::string trim(const std::string& s) {
        size_t start = 0;
        while (start < s.size() && isTrimChar(s[start])) {
            ++start;
        }
        size_t end = s.size();
        while (end > start && isTrimChar(s[end - 1])) {
            --end;
        }
        return s.substr(start, end - start);
    }

    static bool isLetter(char c) {
        return (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z');
    }

public:
    explicit AutomaticGuitarSimulator(std::optional<std::string> text)
        : playText(std::move(text)) {}

    explicit AutomaticGuitarSimulator(const char* text)
        : playText(text ? std::optional<std::string>(text) : std::nullopt) {}

    std::optional<std::vector<ChordTune>> interpret(bool display) const {
        if (!playText.has_value() || trim(*playText).empty()) {
            return std::nullopt;
        }

        std::vector<ChordTune> playList;
        const std::string& text = *playText;
        size_t i = 0;

        while (i <= text.size()) {
            size_t j = text.find(' ', i);
            if (j == std::string::npos) {
                j = text.size();
            }

            std::string playSeg = text.substr(i, j - i);
            if (!trim(playSeg).empty()) {
                int pos = 0;
                for (char ele : playSeg) {
                    if (isLetter(ele)) {
                        ++pos;
                        continue;
                    }
                    break;
                }

                std::string playChord = playSeg.substr(0, pos);
                std::string playValue = playSeg.substr(pos);
                playList.emplace_back(playChord, playValue);

                if (display) {
                    (void)display(playChord, playValue);
                }
            }

            if (j == text.size()) {
                break;
            }
            i = j + 1;
        }

        return playList;
    }

    std::string display(const std::string& key, const std::string& value) const {
        std::ostringstream oss;
        oss << "Normal Guitar Playing -- Chord: " << key << ", Play Tune: " << value;
        return oss.str();
    }
};

namespace std {
    template<>
    struct hash<AutomaticGuitarSimulator::ChordTune> {
        size_t operator()(const AutomaticGuitarSimulator::ChordTune& ct) const noexcept {
            return static_cast<size_t>(ct.hashCode());
        }
    };
}