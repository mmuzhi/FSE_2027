#include <vector>
#include <string>
#include <algorithm>
#include <utility>
#include <stdexcept>
#include <cstddef>

class PushBoxGame {
public:
    std::vector<std::string> map;
    int player_row;
    int player_col;
    std::vector<std::pair<int, int>> targets;
    std::vector<std::pair<int, int>> boxes;
    int target_count;
    bool is_game_over;

    PushBoxGame(const std::vector<std::string>& map)
        : map(map), player_row(0), player_col(0), target_count(0), is_game_over(false) {
        init_game();
    }

    void init_game() {
        for (std::size_t row = 0; row < map.size(); ++row) {
            for (std::size_t col = 0; col < map[row].size(); ++col) {
                char c = map[row][col];
                if (c == 'O') {
                    player_row = static_cast<int>(row);
                    player_col = static_cast<int>(col);
                } else if (c == 'G') {
                    targets.emplace_back(static_cast<int>(row), static_cast<int>(col));
                    ++target_count;
                } else if (c == 'X') {
                    boxes.emplace_back(static_cast<int>(row), static_cast<int>(col));
                }
            }
        }
    }

    bool check_win() {
        int box_on_target_count = 0;
        for (const auto& box : boxes) {
            if (std::find(targets.begin(), targets.end(), box) != targets.end()) {
                ++box_on_target_count;
            }
        }
        if (box_on_target_count == target_count) {
            is_game_over = true;
        }
        return is_game_over;
    }

    bool move(const std::string& direction) {
        int new_player_row = player_row;
        int new_player_col = player_col;

        if (direction == "w") {
            --new_player_row;
        } else if (direction == "s") {
            ++new_player_row;
        } else if (direction == "a") {
            --new_player_col;
        } else if (direction == "d") {
            ++new_player_col;
        }

        if (get_map(new_player_row, new_player_col) != '#') {
            auto box_it = std::find(boxes.begin(), boxes.end(), std::make_pair(new_player_row, new_player_col));
            if (box_it != boxes.end()) {
                int new_box_row = new_player_row + (new_player_row - player_row);
                int new_box_col = new_player_col + (new_player_col - player_col);

                if (get_map(new_box_row, new_box_col) != '#') {
                    boxes.erase(box_it);
                    boxes.emplace_back(new_box_row, new_box_col);
                    player_row = new_player_row;
                    player_col = new_player_col;
                }
            } else {
                player_row = new_player_row;
                player_col = new_player_col;
            }
        }

        return check_win();
    }

private:
    char get_map(int row, int col) const {
        if (row < 0) {
            row += static_cast<int>(map.size());
        }
        if (row < 0 || row >= static_cast<int>(map.size())) {
            throw std::out_of_range("row index out of range");
        }
        const std::string& s = map[row];
        if (col < 0) {
            col += static_cast<int>(s.size());
        }
        if (col < 0 || col >= static_cast<int>(s.size())) {
            throw std::out_of_range("column index out of range");
        }
        return s[col];
    }
};