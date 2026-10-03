#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <stdexcept>

class PushBoxGame {
private:
    std::vector<std::string> map;
    int player_row;
    int player_col;
    std::vector<std::pair<int, int>> targets;
    std::vector<std::pair<int, int>> boxes;
    int target_count;
    bool is_game_over;

    // Helper to access map cell with bounds checking (matching Python IndexError)
    char get_cell(int row, int col) const {
        return map.at(row).at(col);
    }

public:
    PushBoxGame(const std::vector<std::string>& map)
        : map(map), player_row(0), player_col(0), target_count(0), is_game_over(false) {
        init_game();
    }

    void init_game() {
        for (int r = 0; r < static_cast<int>(map.size()); ++r) {
            for (int c = 0; c < static_cast<int>(map[r].size()); ++c) {
                char ch = map[r][c];
                if (ch == 'O') {
                    player_row = r;
                    player_col = c;
                } else if (ch == 'G') {
                    targets.emplace_back(r, c);
                    ++target_count;
                } else if (ch == 'X') {
                    boxes.emplace_back(r, c);
                }
            }
        }
    }

    bool check_win() {
        int box_on_target = 0;
        for (const auto& box : boxes) {
            if (std::find(targets.begin(), targets.end(), box) != targets.end()) {
                ++box_on_target;
            }
        }
        if (box_on_target == target_count) {
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
        } else {
            // Invalid direction – do nothing (Python would also ignore)
            return check_win();
        }

        // Check if the new player cell is not a wall (throws if out of bounds)
        char new_cell = get_cell(new_player_row, new_player_col);
        if (new_cell != '#') {
            auto box_it = std::find(boxes.begin(), boxes.end(),
                                    std::make_pair(new_player_row, new_player_col));
            if (box_it != boxes.end()) {
                // There is a box at the new player position
                int new_box_row = new_player_row + (new_player_row - player_row);
                int new_box_col = new_player_col + (new_player_col - player_col);

                // Check if the box's new position is not a wall (throws if out of bounds)
                char new_box_cell = get_cell(new_box_row, new_box_col);
                if (new_box_cell != '#') {
                    // Move box
                    boxes.erase(box_it);
                    boxes.emplace_back(new_box_row, new_box_col);
                    // Move player
                    player_row = new_player_row;
                    player_col = new_player_col;
                } else {
                    // Box cannot move into wall – player does not move
                    // (nothing changes)
                }
            } else {
                // No box, just move player
                player_row = new_player_row;
                player_col = new_player_col;
            }
        }
        // If the new cell is a wall (or out of bounds) no movement occurs

        return check_win();
    }
};