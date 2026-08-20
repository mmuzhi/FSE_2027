#include <algorithm>
#include <cstddef>
#include <string>
#include <utility>
#include <vector>

class PushBoxGame {
public:
    std::vector<std::string> map;
    int player_row;
    int player_col;
    std::vector<std::pair<int, int> > targets;
    std::vector<std::pair<int, int> > boxes;
    int target_count;
    bool is_game_over;

    // Initialize the push box game with the map and various attributes.
    PushBoxGame(const std::vector<std::string>& map)
        : map(map),
          player_row(0),
          player_col(0),
          targets(),
          boxes(),
          target_count(0),
          is_game_over(false) {
        init_game();
    }

    // Initialize the game by locating the player ('O'), targets ('G')
    // and boxes ('X') on the map.
    void init_game() {
        for (std::size_t row = 0; row < map.size(); ++row) {
            const std::string& line = map[row];
            for (std::size_t col = 0; col < line.size(); ++col) {
                const char cell = line[col];
                if (cell == 'O') {
                    player_row = static_cast<int>(row);
                    player_col = static_cast<int>(col);
                } else if (cell == 'G') {
                    targets.push_back(std::make_pair(static_cast<int>(row),
                                                     static_cast<int>(col)));
                    ++target_count;
                } else if (cell == 'X') {
                    boxes.push_back(std::make_pair(static_cast<int>(row),
                                                   static_cast<int>(col)));
                }
            }
        }
    }

    // Check if the game is won: every box is on a target position.
    // Updates is_game_over and returns it.
    bool check_win() {
        int box_on_target_count = 0;
        for (std::vector<std::pair<int, int> >::const_iterator it = boxes.begin();
             it != boxes.end(); ++it) {
            if (std::find(targets.begin(), targets.end(), *it) != targets.end()) {
                ++box_on_target_count;
            }
        }
        if (box_on_target_count == target_count) {
            is_game_over = true;
        }
        return is_game_over;
    }

    // Move the player in the given direction ("w", "s", "a" or "d"),
    // pushing a box if one is in the way, then check whether the game is won.
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
            const std::pair<int, int> new_pos(new_player_row, new_player_col);
            std::vector<std::pair<int, int> >::iterator box_it =
                std::find(boxes.begin(), boxes.end(), new_pos);
            if (box_it != boxes.end()) {
                int new_box_row = new_player_row + (new_player_row - player_row);
                int new_box_col = new_player_col + (new_player_col - player_col);

                if (map[new_box_row][new_box_col] != '#') {
                    boxes.erase(box_it);
                    boxes.push_back(std::make_pair(new_box_row, new_box_col));
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

    // Convenience overload: allows the direction to be passed as a single
    // character, e.g. move('d'), behaving exactly like move("d").
    bool move(char direction) {
        return move(std::string(1, direction));
    }
};