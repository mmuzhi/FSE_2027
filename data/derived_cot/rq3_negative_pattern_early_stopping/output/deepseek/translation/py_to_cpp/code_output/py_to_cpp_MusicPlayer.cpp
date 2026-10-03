#include <vector>
#include <string>
#include <optional>
#include <variant>
#include <algorithm>
#include <random>
#include <chrono>

class MusicPlayer {
public:
    MusicPlayer() : volume(50) {}

    void add_song(const std::string& song) {
        playlist.push_back(song);
    }

    void remove_song(const std::string& song) {
        auto it = std::find(playlist.begin(), playlist.end(), song);
        if (it != playlist.end()) {
            playlist.erase(it);
            if (current_song.has_value() && current_song.value() == song) {
                stop();
            }
        }
    }

    std::variant<std::string, bool, std::monostate> play() {
        if (!playlist.empty() && current_song.has_value()) {
            return playlist[0];
        } else if (!playlist.empty()) {
            return false;
        } else {
            return std::monostate{};
        }
    }

    bool stop() {
        if (current_song.has_value()) {
            current_song.reset();
            return true;
        }
        return false;
    }

    bool switch_song() {
        if (current_song.has_value()) {
            auto it = std::find(playlist.begin(), playlist.end(), current_song.value());
            if (it != playlist.end()) {
                int idx = std::distance(playlist.begin(), it);
                if (idx < static_cast<int>(playlist.size()) - 1) {
                    current_song = playlist[idx + 1];
                    return true;
                }
            }
        }
        return false;
    }

    bool previous_song() {
        if (current_song.has_value()) {
            auto it = std::find(playlist.begin(), playlist.end(), current_song.value());
            if (it != playlist.end()) {
                int idx = std::distance(playlist.begin(), it);
                if (idx > 0) {
                    current_song = playlist[idx - 1];
                    return true;
                }
            }
        }
        return false;
    }

    std::variant<std::monostate, bool> set_volume(int vol) {
        if (vol >= 0 && vol <= 100) {
            volume = vol;
            return std::monostate{};
        } else {
            return false;
        }
    }

    bool shuffle() {
        if (playlist.empty()) {
            return false;
        }
        unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
        std::shuffle(playlist.begin(), playlist.end(), std::default_random_engine(seed));
        return true;
    }

private:
    std::vector<std::string> playlist;
    std::optional<std::string> current_song;
    int volume;
};