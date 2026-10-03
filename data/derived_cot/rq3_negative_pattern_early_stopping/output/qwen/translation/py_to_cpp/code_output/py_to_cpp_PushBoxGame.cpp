#include <vector>
#include <string>
#include <utility> // for std::pair

class PushBoxGame {
private:
    std::vector<std::string> map_;
    int player_row;
    int player_col;
    std::vector<std::pair<int, int>> targets;
    std::vector<std::pair<int, int>> boxes;
    int target_count;
    bool is_game_over;

    void init_game() {
        for (int row = 0; row < map_.size(); ++row) {
            for (int col = 0; col < map_[row].size(); ++col) {
                if (map_[row][col] == 'O') {
                    player_row = row;
                    player_col = col;
                } else if (map_[row][col] == 'G') {
                    targets.push_back(std::make_pair(row, col));
                    ++target_count;
                } else if (map_[row][col] == 'X') {
                    boxes.push_back(std::make_pair(row, col));
                }
            }
        }
    }

public:
    PushBoxGame(const std::vector<std::string>& map) : 
        map_(map), 
        player_row(0), 
        player_col(0), 
        target_count(0), 
        is_game_over(false) {
        init_game();
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

    bool move(char direction) {
        int new_player_row = player_row;
        int new_player_col = player_col;

        switch (direction) {
            case 'w': --new_player_row; break;
            case 's': ++new_player_row; break;
            case 'a': --new_player_col; break;
            case 'd': ++new_player_col; break;
            default: break; // Handle invalid direction if necessary
        }

        if (map_[new_player_row][new_player_col] == '#') {
            return false;
        }

        if (std::find(boxes.begin(), boxes.end(), std::make_pair(new_player_row, new_player_col)) != boxes.end()) {
            int new_box_row = new_player_row + (new_player_row - player_row);
            int new_box_col = new_player_col + (new_player_col - player_col);

            if (map_[new_box_row][new_box_col] == '#') {
                return false;
            }

            // Remove the box from its current position
            auto it = std::find(boxes.begin(), boxes.end(), std::make_pair(new_player_row, new_player_col));
            boxes.erase(it);

            // Add the box at the new position
            boxes.push_back(std::make_pair(new_box_row, new_box_col));
        }

        player_row = new_player_row;
        player_col = new_player_col;

        return check_win();
    }
};