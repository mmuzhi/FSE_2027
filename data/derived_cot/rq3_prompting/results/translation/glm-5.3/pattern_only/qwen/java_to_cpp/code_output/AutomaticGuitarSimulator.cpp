#pragma once

#include <cctype>
#include <cstdint>
#include <functional>
#include <optional>
#include <string>
#include <utility>
#include <vector>

namespace org::example {

class AutomaticGuitarSimulator {
public:
    // Maps Java's public static nested class ChordTune.
    class ChordTune {
    public:
        ChordTune(std::string chord, std::string tune)
            : chord_(std::move(chord)), tune_(std::move(tune)) {}

        const std::string& getChord() const { return chord_; }
        const std::string& getTune() const { return tune_; }

        // Java equals(): same runtime type + field equality.
        bool operator==(const ChordTune& that) const {
            return chord_ == that.chord_ && tune_ == that.tune_;
        }
        bool operator!=(const ChordTune& that) const { return !(*this == that); }

    private:
        std::string chord_;
        std::string tune_;
    };

    explicit AutomaticGuitarSimulator(std::string text)
        : playText_(std::move(text)) {}

    // Java returns null on null/blank input -> std::nullopt here.
    std::optional<std::vector<ChordTune>> interpret(bool display) const {
        // Java: playText == null || playText.trim().isEmpty()
        // (std::string cannot be null; blank check covers the rest).
        if (trim(playText_).empty()) {
            return std::nullopt;
        }

        std::vector<ChordTune> playList;
        std::vector<std::string> playSegs = splitOnSpace(playText_);
        for (const std::string& playSeg : playSegs) {
            if (trim(playSeg).empty()) {
                continue;
            }
            std::size_t pos = 0;
            for (char ele : playSeg) {
                // Character.isLetter -> std::isalpha for ASCII input.
                // unsigned char cast avoids UB on negative char values.
                if (std::isalpha(static_cast<unsigned char>(ele))) {
                    ++pos;
                    continue;
                }
                break;
            }
            std::string playChord = playSeg.substr(0, pos);
            std::string playValue = playSeg.substr(pos);
            playList.emplace_back(playChord, playValue);
            if (display) {
                // Java discards the return value here; keep identical (no printing).
                static_cast<void>(this->display(playChord, playValue));
            }
        }
        return playList;
    }

    std::string display(const std::string& key, const std::string& value) const {
        return "Normal Guitar Playing -- Chord: " + key + ", Play Tune: " + value;
    }

private:
    std::string playText_;

    // Java String.trim(): removes leading/trailing chars with code <= U+0020.
    static std::string trim(const std::string& s) {
        std::size_t begin = 0;
        std::size_t end = s.size();
        while (begin < end && static_cast<unsigned char>(s[begin]) <= ' ') ++begin;
        while (end > begin && static_cast<unsigned char>(s[end - 1]) <= ' ') --end;
        return s.substr(begin, end - begin);
    }

    // Java String.split(" "): split on the single space char only
    // (NOT all whitespace), with trailing empty segments dropped.
    static std::vector<std::string> splitOnSpace(const std::string& s) {
        std::vector<std::string> parts;
        std::string current;
        for (char c : s) {
            if (c == ' ') {
                parts.push_back(current);
                current.clear();
            } else {
                current += c;
            }
        }
        parts.push_back(current);
        // Java split(regex, limit=0) removes trailing empty strings.
        while (!parts.empty() && parts.back().empty()) {
            parts.pop_back();
        }
        return parts;
    }
};

}  // namespace org::example

// Mirrors Java hashCode() contract: equal objects -> equal hashes,
// with the same 31-based computation (32-bit wrap like Java int).
namespace std {
template <>
struct hash<org::example::AutomaticGuitarSimulator::ChordTune> {
    std::size_t operator()(
        const org::example::AutomaticGuitarSimulator::ChordTune& ct) const {
        auto javaStringHash = [](const std::string& s) -> std::uint32_t {
            std::uint32_t h = 0;
            for (char c : s) {
                // Java char acts as unsigned; replicate via unsigned char.
                h = 31u * h + static_cast<unsigned char>(c);
            }
            return h;
        };
        std::uint32_t result = javaStringHash(ct.getChord());
        result = 31u * result + javaStringHash(ct.getTune());
        return static_cast<std::size_t>(result);
    }
};
}  // namespace std