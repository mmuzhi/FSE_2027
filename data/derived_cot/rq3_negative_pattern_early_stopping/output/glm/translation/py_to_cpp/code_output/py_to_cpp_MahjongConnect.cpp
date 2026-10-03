#include <vector>
#include <string>
#include <random>
#include <set>
#include <utility>

class MahjongConnect {
public:
    std::vector<int> BOARD_SIZE;
    std::vector<std::string> ICONS;
    std::vector<std::vector<std::string>> board;

    MahjongConnect(std::vector<int> BOARD_SIZE, std::vector<std::string> ICONS)
        : BOARD_SIZE(std::move(BOARD_SIZE)), ICONS(std::move(ICONS)) {
        board = create_board();
    }

    std::vector<std::vector<std::string>> create_board() {
        std::vector<std::vector<std::string>> b(BOARD_SIZE[0], std::vector<std::string>(BOARD_SIZE[1]));
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distrib(0, ICONS.size() - 1);
        
        for (int i = 0; i < BOARD_SIZE[0]; ++i) {
            for (int j = 0; j < BOARD_SIZE[1]; ++j) {
                b[i][j] = ICONS[distrib(gen)];
            }
        }
        return b;
    }

    bool is_valid_move(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        int x1 = pos1.first, y1 = pos1.second;
        int x2 = pos2.first, y2 = pos2.second;

        // Check if positions are within the game board range
        if (!(0 <= x1 && x1 < BOARD_SIZE[0] && 0 <= y1 && y1 < BOARD_SIZE[1] &&
              0 <= x2 && x2 < BOARD_SIZE[0] && 0 <= y2 && y2 < BOARD_SIZE[1])) {
            return false;
        }

        // Check if the two positions are the same
        if (pos1 == pos2) {
            return false;
        }

        // Check if the two positions have the same icon
        if (board[x1][y1] != board[x2][y2]) {
            return false;
        }

        // Check if there is a valid path between the two positions
        if (!has_path(pos1, pos2)) {
            return false;
        }

        return true;
    }

    bool has_path(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        std::set<std::pair<int, int>> visited;
        std::vector<std::pair<int, int>> stack;
        stack.push_back(pos1);

        while (!stack.empty()) {
            std::pair<int, int> current_pos = stack.back();
            stack.pop_back();

            if (current_pos == pos2) {
                return true;
            }

            if (visited.count(current_pos)) {
                continue;
            }

            visited.insert(current_pos);
            int x = current_pos.first;
            int y = current_pos.second;

            // Check adjacent positions (up, down, left, right)
            std::vector<std::pair<int, int>> directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
            for (const auto& dir : directions) {
                int new_x = x + dir.first;
                int new_y = y + dir.second;
                if (0 <= new_x && new_x < BOARD_SIZE[0] && 0 <= new_y && new_y < BOARD_SIZE[1]) {
                    if (!visited.count({new_x, new_y}) && board[new_x][new_y] == board[x][y]) {
                        stack.push_back({new_x, new_y});
                    }
                }
            }
        }

        return false;
    }

    void remove_icons(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        int x1 = pos1.first, y1 = pos1.second;
        int x2 = pos2.first, y2 = pos2.second;
        board[x1][y1] = " ";
        board[x2][y2] = " ";
    }

    bool is_game_over() {
        for (const auto& row : board) {
            for (const auto& icon : row) {
                if (icon != " ") {
                    return false;
                }
            }
        }
        return true;
    }
};