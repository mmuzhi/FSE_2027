#include <cstddef>
#include <random>
#include <stdexcept>
#include <utility>
#include <vector>
#include <string>

class MahjongConnect {
public:
    std::vector<int> BOARD_SIZE;
    std::vector<std::string> ICONS;
    std::vector<std::vector<std::string>> board;

    MahjongConnect(std::vector<int> boardSize, std::vector<std::string> icons)
        : BOARD_SIZE(std::move(boardSize)), ICONS(std::move(icons)),
          board(create_board()) {}

    std::vector<std::vector<std::string>> create_board() {
        static std::mt19937 rng(std::random_device{}());
        std::uniform_int_distribution<std::size_t> dist(0, ICONS.size() - 1);
        std::vector<std::vector<std::string>> result;
        result.reserve(static_cast<std::size_t>(BOARD_SIZE[0]));
        for (int i = 0; i < BOARD_SIZE[0]; ++i) {
            std::vector<std::string> row;
            row.reserve(static_cast<std::size_t>(BOARD_SIZE[1]));
            for (int j = 0; j < BOARD_SIZE[1]; ++j) {
                row.push_back(ICONS[dist(rng)]);
            }
            result.push_back(std::move(row));
        }
        return result;
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
        std::vector<std::vector<bool>> visited(
            static_cast<std::size_t>(BOARD_SIZE[0]),
            std::vector<bool>(static_cast<std::size_t>(BOARD_SIZE[1]), false));
        std::vector<std::pair<int, int>> stack;
        stack.push_back(pos1);

        static const int dx[4] = {0, 0, 1, -1};
        static const int dy[4] = {1, -1, 0, 0};

        while (!stack.empty()) {
            std::pair<int, int> current_pos = stack.back();
            stack.pop_back();
            if (current_pos == pos2) {
                return true;
            }

            if (visited[current_pos.first][current_pos.second]) {
                continue;
            }

            visited[current_pos.first][current_pos.second] = true;
            int x = current_pos.first, y = current_pos.second;

            // Check adjacent positions (up, down, left, right)
            for (int d = 0; d < 4; ++d) {
                int new_x = x + dx[d], new_y = y + dy[d];
                if (0 <= new_x && new_x < BOARD_SIZE[0] && 0 <= new_y && new_y < BOARD_SIZE[1]) {
                    if (!visited[new_x][new_y] && board[new_x][new_y] == board[x][y]) {
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
        board.at(x1).at(y1) = " ";
        board.at(x2).at(y2) = " ";
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