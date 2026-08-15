#include <vector>
#include <string>
#include <optional>
#include <variant>
#include <algorithm>
#include <random>
#include <stdexcept>

class MusicPlayer {
public:
    MusicPlayer();

    void add_song(const std::string& song);
    void remove_song(const std::string& song);
    std::variant<std::string, bool, std::monostate> play();
    bool stop();
    bool switch_song();
    bool previous_song();
    std::optional<bool> set_volume(int volume);
    bool shuffle();

private:
    std::vector<std::string> playlist;
    std::optional<std::string> current_song;
    int volume;
};

MusicPlayer::MusicPlayer() : volume(50) {}

void MusicPlayer::add_song(const std::string& song) {
    playlist.push_back(song);
}

void MusicPlayer::remove_song(const std::string& song) {
    auto it = std::find(playlist.begin(), playlist.end(), song);
    if (it != playlist.end()) {
        playlist.erase(it);
        if (current_song.has_value() && *current_song == song) {
            stop();
        }
    }
}

std::variant<std::string, bool, std::monostate> MusicPlayer::play() {
    if (!playlist.empty() && current_song.has_value() && !current_song->empty()) {
        return playlist[0];
    } else if (!playlist.empty()) {
        return false;
    } else {
        return std::monostate{};
    }
}

bool MusicPlayer::stop() {
    if (current_song.has_value() && !current_song->empty()) {
        current_song.reset();
        return true;
    }
    return false;
}

bool MusicPlayer::switch_song() {
    if (current_song.has_value() && !current_song->empty()) {
        auto it = std::find(playlist.begin(), playlist.end(), *current_song);
        if (it == playlist.end()) {
            throw std::out_of_range("current_song not in playlist");
        }
        size_t current_index = static_cast<size_t>(std::distance(playlist.begin(), it));
        if (current_index < playlist.size() - 1) {
            current_song = playlist[current_index + 1];
            return true;
        }
        return false;
    }
    return false;
}

bool MusicPlayer::previous_song() {
    if (current_song.has_value() && !current_song->empty()) {
        auto it = std::find(playlist.begin(), playlist.end(), *current_song);
        if (it == playlist.end()) {
            throw std::out_of_range("current_song not in playlist");
        }
        size_t current_index = static_cast<size_t>(std::distance(playlist.begin(), it));
        if (current_index > 0) {
            current_song = playlist[current_index - 1];
            return true;
        }
        return false;
    }
    return false;
}

std::optional<bool> MusicPlayer::set_volume(int volume) {
    if (volume >= 0 && volume <= 100) {
        this->volume = volume;
        return std::nullopt;
    }
    return false;
}

bool MusicPlayer::shuffle() {
    if (!playlist.empty()) {
        std::random_device rd;
        std::mt19937 g(rd());
        std::shuffle(playlist.begin(), playlist.end(), g);
        return true;
    }
    return false;
}