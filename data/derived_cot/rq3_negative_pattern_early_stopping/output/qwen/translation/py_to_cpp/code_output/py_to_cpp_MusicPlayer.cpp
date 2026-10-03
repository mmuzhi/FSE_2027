#include <vector>
#include <string>
#include <variant>
#include <algorithm>
#include <iostream>

using namespace std;

class MusicPlayer {
private:
    vector<string> playlist;
    string current_song;
    int volume;

public:
    MusicPlayer() : playlist(), current_song(), volume(50) {}

    void add_song(const string& song) {
        playlist.push_back(song);
    }

    void remove_song(const string& song) {
        if (song == current_song) {
            this->stop();
        }
        auto it = find(playlist.begin(), playlist.end(), song);
        if (it != playlist.end()) {
            playlist.erase(it);
        }
    }

    variant<string, bool, monostate> play() {
        if (!playlist.empty() && !current_song.empty()) {
            return playlist[0];
        } else if (!playlist.empty()) {
            return false;
        } else {
            return monostate();
        }
    }

    bool stop() {
        if (!current_song.empty()) {
            current_song = "";
            return true;
        }
        return false;
    }

    bool switch_song() {
        if (current_song.empty()) {
            return false;
        }
        auto it = find(playlist.begin(), playlist.end(), current_song);
        if (it == playlist.end()) {
            return false;
        }
        size_t index = distance(playlist.begin(), it);
        if (index < playlist.size() - 1) {
            current_song = playlist[index + 1];
            return true;
        }
        return false;
    }

    bool previous_song() {
        if (current_song.empty()) {
            return false;
        }
        auto it = find(playlist.begin(), playlist.end(), current_song);
        if (it == playlist.end()) {
            return false;
        }
        size_t index = distance(playlist.begin(), it);
        if (index > 0) {
            current_song = playlist[index - 1];
            return true;
        }
        return false;
    }

    bool set_volume(int volume) {
        if (volume < 0 || volume > 100) {
            return false;
        }
        this->volume = volume;
        return true;
    }

    bool shuffle() {
        if (playlist.empty()) {
            return false;
        }
        random_shuffle(playlist.begin(), playlist.end());
        return true;
    }
};