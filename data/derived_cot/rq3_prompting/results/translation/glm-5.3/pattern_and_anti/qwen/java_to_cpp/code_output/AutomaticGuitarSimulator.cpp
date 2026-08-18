#pragma once
#include <cctype>
#include <cstdint>
#include <functional>
#include <optional>
#include <string>
#include <utility>
#include <vector>

namespace org {
namespace example {

class AutomaticGuitarSimulator {
public:
    class ChordTune {
    public:
        ChordTune(std::string chord, std::string tune)
            : chord_(std::move(chord)), tune_(std::move(tune)) {}

        const std::string& getChord() const { return chord_; }
        const std::string& getTune() const { return tune_; }

        bool operator==(const ChordTune& other) const {
            return chord_ == other.chord_ && tune_ == other.tune_;
        }

        bool operator!=(const ChordTune& other) const {
            return !(*this == other);
        }

        // Mirrors Java: 31 * result + tune.hashCode(), with Java-style
        // 32-bit wrapping String hash (not observable via I/O).
        int32_t hashCode() const {
            uint32_t result = javaStringHash(chord_);
            result = 31u * result + javaStringHash(tune_);
            return static_cast<int32_t>(result);
        }

    private:
        static uint32_t javaStringHash(const std::string& s) {
            uint32_t h = 0;
            for (unsigned char c : s) {
                h = 31u * h + c;
            }
            return h;
        }

        std::string chord_;
        std::string tune_;
    };

    explicit AutomaticGuitarSimulator(std::string text)
        : playText_(std::move(text)) {}

    // Java returns null on empty/whitespace input; mapped to std::nullopt.
    std::optional<std::vector<ChordTune>> interpret(bool display) {
        if (trim(playText_).empty()) {
            return std::nullopt;
        }

        std::vector<ChordTune> playList;
        std::vector<std::string> playSegs = split(playText_, ' ');
        for (const std::string& playSeg : playSegs) {
            if (trim(playSeg).empty()) {
                continue;
            }
            std::size_t pos = 0;
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
                // Java discards the return value here as well (no printing).
                display(playChord, playValue);
            }
        }
        return playList;
    }

    std::string display(const std::string& key, const std::string& value) {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }

private:
    static std::string trim(const std::string& s) {
        std::size_t start = 0;
        while (start < s.size() &&
               std::isspace(static_cast<unsigned char>(s[start]))) {
            ++start;
        }
        std::size_t end = s.size();
        while (end > start &&
               std::isspace(static_cast<unsigned char>(s[end - 1]))) {
            --end;
        }
        return s.substr(start, end - start);
    }

    // Mirrors Java's String.split(" "): interior empty segments are kept,
    // trailing empty segments are removed. (Interior empties are skipped
    // by the trim().isEmpty() check, so behavior matches either way.)
    static std::vector<std::string> split(const std::string& s, char delim) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : s) {
            if (c == delim) {
                parts.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        parts.push_back(current);
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }

    std::string playText_;
};

} // namespace example
} // namespace org

namespace std {
template <>
struct hash<org::example::AutomaticGuitarSimulator::ChordTune> {
    std::size_t operator()(
        const org::example::AutomaticGuitarSimulator::ChordTune& ct) const noexcept {
        return static_cast<std::size_t>(ct.hashCode());
    }
};
} // namespace std