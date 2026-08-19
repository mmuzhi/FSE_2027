#include <algorithm>
#include <random>
#include <stdexcept>
#include <string>
#include <variant>
#include <vector>
#include <optional>

class MusicPlayer {
public:
    std::vector<std::string> playlist;
    std::optional<std::string> current_song;  // Python None -> nullopt
    int volume = 50;

    MusicPlayer() = default;

    void add_song(const std::string& song) {
        playlist.push_back(song);
    }

    void remove_song(const std::string& song) {
        auto it = std::find(playlist.begin(), playlist.end(), song);
        if (it != playlist.end()) {
            playlist.erase(it);
            if (current_song && *current_song == song)
                stop();
        }
    }

    // Returns: the song (str), False, or None (monostate) — mirrors Python return paths.
    std::variant<std::monostate, bool, std::string> play() {
        if (!playlist.empty() && truthy(current_song))
            return playlist[0];
        else if (!playlist.empty())
            return false;
        return std::monostate{};  // None
    }

    bool stop() {
        if (truthy(current_song)) {
            current_song.reset();
            return true;
        }
        return false;
    }

    bool switch_song() {
        if (truthy(current_song)) {
            auto it = std::find(playlist.begin(), playlist.end(), *current_song);
            if (it == playlist.end())
                throw std::invalid_argument(*current_song + " is not in list");  // ValueError
            std::size_t current_index = static_cast<std::size_t>(it - playlist.begin());
            if (current_index < playlist.size() - 1) {
                current_song = playlist[current_index + 1];
                return true;
            }
            return false;
        }
        return false;
    }

    bool previous_song() {
        if (truthy(current_song)) {
            auto it = std::find(playlist.begin(), playlist.end(), *current_song);
            if (it == playlist.end())
                throw std::invalid_argument(*current_song + " is not in list");  // ValueError
            std::size_t current_index = static_cast<std::size_t>(it - playlist.begin());
            if (current_index > 0) {
                current_song = playlist[current_index - 1];
                return true;
            }
            return false;
        }
        return false;
    }

    // Returns None on success, False on invalid volume.
    std::variant<std::monostate, bool> set_volume(int new_volume) {
        if (0 <= new_volume && new_volume <= 100) {
            volume = new_volume;
            return std::monostate{};  // None
        }
        return false;
    }

    bool shuffle() {
        if (!playlist.empty()) {
            std::random_device rd;
            std::mt19937 g(rd());
            std::shuffle(playlist.begin(), playlist.end(), g);
            return true;
        }
        return false;
    }

private:
    // Python string truthiness: only non-empty strings are truthy.
    static bool truthy(const std::optional<std::string>& s) {
        return s.has_value() && !s->empty();
    }
};