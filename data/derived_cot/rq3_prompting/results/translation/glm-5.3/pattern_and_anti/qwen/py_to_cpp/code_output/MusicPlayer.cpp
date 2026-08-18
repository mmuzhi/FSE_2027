#include <vector>
#include <string>
#include <optional>
#include <algorithm>
#include <random>
#include <stdexcept>

class MusicPlayer {
public:
    std::vector<std::string> playlist;
    std::optional<std::string> current_song;
    int volume;

    MusicPlayer() : volume(50) {}

    void add_song(const std::string& song) {
        playlist.push_back(song);
    }

    void remove_song(const std::string& song) {
        auto it = std::find(playlist.begin(), playlist.end(), song);
        if (it != playlist.end()) {
            playlist.erase(it);
            if (current_song.has_value() && *current_song == song) {
                stop();
            }
        }
    }

    std::optional<std::string> play() {
        if (!playlist.empty() && current_song.has_value()) {
            return playlist[0];
        } else if (!playlist.empty()) {
            return std::nullopt;  // False
        }
        return std::nullopt;      // None
    }

    bool stop() {
        if (current_song.has_value()) {
            current_song.reset();
            return true;
        } else {
            return false;
        }
    }

    bool switch_song() {
        if (current_song.has_value()) {
            auto it = std::find(playlist.begin(), playlist.end(), *current_song);
            if (it == playlist.end()) {
                throw std::invalid_argument("ValueError: current_song is not in playlist");
            }
            int current_index = static_cast<int>(std::distance(playlist.begin(), it));
            if (current_index < static_cast<int>(playlist.size()) - 1) {
                current_song = playlist[current_index + 1];
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    bool previous_song() {
        if (current_song.has_value()) {
            auto it = std::find(playlist.begin(), playlist.end(), *current_song);
            if (it == playlist.end()) {
                throw std::invalid_argument("ValueError: current_song is not in playlist");
            }
            int current_index = static_cast<int>(std::distance(playlist.begin(), it));
            if (current_index > 0) {
                current_song = playlist[current_index - 1];
                return true;
            } else {
                return false;
            }
        } else {
            return false;
        }
    }

    bool set_volume(int volume) {
        if (0 <= volume && volume <= 100) {
            this->volume = volume;
            return true;
        } else {
            return false;
        }
    }

    bool shuffle() {
        if (!playlist.empty()) {
            std::random_device rd;
            std::mt19937 g(rd());
            std::shuffle(playlist.begin(), playlist.end(), g);
            return true;
        } else {
            return false;
        }
    }
};