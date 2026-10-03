#include <vector>
#include <string>
#include <utility>
#include <algorithm>

class PushBoxGame {
public:
    std::vector<std::string> map;
    int player_row;
    int player_col;
    std::vector<std::pair<int, int>> targets;
    std::vector<std::pair<int, int>> boxes;
    int target_count;
    bool is_game_over;

    PushBoxGame(std::vector<std::string> map)
        : map(std::move(map)), player_row(0), player_col(0), target_count(0), is_game_over(false) {
        init_game();
    }

    void init_game() {
        for (int row = 0; row < static_cast<int>(map.size()); ++row) {
            for (int col = 0; col < static_cast<int>(map[row].size()); ++col) {
                if (map[row][col] == 'O') {
                    player_row = row;
                    player_col = col;
                } else if (map[row][col] == 'G') {
                    targets.emplace_back(row, col);
                    target_count += 1;
                } else if (map[row][col] == 'X') {
                    boxes.emplace_back(row, col);
                }
            }
        }
    }

    bool check_win() {
        int box_on_target_count = 0;
        for (const auto& box : boxes) {
            if (std::find(targets.begin(), targets.end(), box) != targets.end()) {
                box_on_target_count += 1;
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
            new_player_row -= 1;
        } else if (direction == "s") {
            new_player_row += 1;
        } else if (direction == "a") {
            new_player_col -= 1;
        } else if (direction == "d") {
            new_player_col += 1;
        }

        if (map[new_player_row][new_player_col] != '#') {
            auto it = std::find(boxes.begin(), boxes.end(), std::make_pair(new_player_row, new_player_col));
            if (it != boxes.end()) {
                int new_box_row = new_player_row + (new_player_row - player_row);
                int new_box_col = new_player_col + (new_player_col - player_col);

                if (map[new_box_row][new_box_col] != '#') {
                    boxes.erase(it);
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
};