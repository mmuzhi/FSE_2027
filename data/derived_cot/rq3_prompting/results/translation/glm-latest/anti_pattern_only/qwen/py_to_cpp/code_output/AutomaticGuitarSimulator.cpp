#include <cctype>
#include <string>
#include <utility>
#include <vector>

/**
 * This class is an automatic guitar simulator that can interpret and play
 * based on the input guitar sheet music.
 */
class AutomaticGuitarSimulator {
public:
    // Equivalent of the Python dict with two fields, Chord and Tune,
    // which are letters and numbers, respectively.
    struct PlayItem {
        std::string Chord;
        std::string Tune;
    };

    /**
     * Initialize the score to be played
     * :param text: str, score to be played
     */
    explicit AutomaticGuitarSimulator(std::string text)
        : play_text(std::move(text)) {}

    /**
     * Interpret the music score to be played
     * :param display: bool, representing whether to print the interpreted score
     * :return: vector of PlayItem. If the input is empty or contains only
     *          whitespace, an empty vector is returned.
     */
    std::vector<PlayItem> interpret(bool display = false) const {
        // Python: if not self.play_text.strip(): return []
        if (is_blank(play_text)) {
            return {};
        }

        std::vector<PlayItem> play_list;
        std::vector<std::string> play_segs = split(play_text, ' ');
        play_list.reserve(play_segs.size());

        for (const std::string& play_seg : play_segs) {
            // Count the leading alphabetic characters.
            std::string::size_type pos = 0;
            for (char ele : play_seg) {
                if (std::isalpha(static_cast<unsigned char>(ele))) {
                    ++pos;
                    continue;
                }
                break;
            }

            std::string play_chord = play_seg.substr(0, pos);
            std::string play_value = play_seg.substr(pos);
            play_list.push_back({play_chord, play_value});

            if (display) {
                // Same as Python: the returned string is discarded
                // (display itself does not print anything).
                static_cast<void>(this->display(play_chord, play_value));
            }
        }
        return play_list;
    }

    /**
     * Return chord and play tune with following format:
     *   Normal Guitar Playing -- Chord: %s, Play Tune: %s
     * :param key: str, chord
     * :param value: str, play tune
     * :return: str
     */
    std::string display(const std::string& key, const std::string& value) const {
        return "Normal Guitar Playing -- Chord: " + key +
               ", Play Tune: " + value;
    }

private:
    std::string play_text;

    // Equivalent of Python's `not text.strip()` (empty or all-whitespace).
    static bool is_blank(const std::string& s) {
        for (char c : s) {
            if (std::isspace(static_cast<unsigned char>(c)) == 0) {
                return false;
            }
        }
        return true;
    }

    // Equivalent of Python's `text.split(" ")`: every single occurrence of
    // the separator yields an element, so empty segments are preserved
    // (e.g. "a  b" -> {"a", "", "b"}, "a " -> {"a", ""}).
    static std::vector<std::string> split(const std::string& s, char sep) {
        std::vector<std::string> parts;
        std::string::size_type start = 0;
        while (true) {
            const std::string::size_type end = s.find(sep, start);
            if (end == std::string::npos) {
                parts.push_back(s.substr(start));
                break;
            }
            parts.push_back(s.substr(start, end - start));
            start = end + 1;
        }
        return parts;
    }
};