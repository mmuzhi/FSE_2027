#include <vector>
#include <random>
#include <utility> // for std::pair
#include <set>

class MahjongConnect {
private:
    std::vector<std::vector<char>> board;
    std::vector<int> BOARD_SIZE;
    std::vector<char> ICONS;

    std::pair<int, int> pos1;
    std::pair<int, int> pos2;

    bool has_path(std::pair<int, int> start, std::pair<int, int> end) {
        std::set<std::pair<int, int>> visited;
        std::vector<std::pair<int, int>> stack;
        stack.push_back(start);

        while (!stack.empty()) {
            auto current = stack.back();
            stack.pop_back();

            if (current == end) {
                return true;
            }

            if (visited.find(current) != visited.end()) {
                continue;
            }

            visited.insert(current);
            int x = current.first;
            int y = current.second;

            for (const auto& dir : std::vector<std::pair<int, int>>{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}) {
                int new_x = x + dir.first;
                int new_y = y + dir.second;
                if (new_x >= 0 && new_x < BOARD_SIZE[0] && new_y >= 0 && new_y < BOARD_SIZE[1]) {
                    if (visited.find({new_x, new_y}) == visited.end() && 
                        board[new_x][new_y] == board[x][y]) {
                        stack.push_back({new_x, new_y});
                    }
                }
            }
        }

        return false;
    }

public:
    MahjongConnect(const std::vector<int>& board_size, const std::vector<char>& icons) {
        BOARD_SIZE = board_size;
        ICONS = icons;
        board = create_board();
    }

    std::vector<std::vector<char>> create_board() {
        std::vector<std::vector<char>> board(BOARD_SIZE[0], std::vector<char>(BOARD_SIZE[1], ' '));
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distrib(0, ICONS.size() - 1);

        for (int i = 0; i < BOARD_SIZE[0]; ++i) {
            for (int j = 0; j < BOARD_SIZE[1]; ++j) {
                board[i][j] = ICONS[distrib(gen)];
            }
        }
        return board;
    }

    bool is_valid_move(const std::pair<int, int>& pos1, const std::pair<int, int>& pos2) {
        int x1 = pos1.first, y1 = pos1.second;
        int x2 = pos2.first, y2 = pos2.second;

        // Check if positions are within bounds
        if (x1 < 0 || x1 >= BOARD_SIZE[0] || y1 < 0 || y1 >= BOARD_SIZE[1] ||
            x2 < 0 || x2 >= BOARD_SIZE[0] || y2 < 0 || y2 >= BOARD_SIZE[1]) {
            return false;
        }

        // Check if positions are the same
        if (pos1 == pos2) {
            return false;
        }

        // Check if icons are the same
        if (board[x1][y1] != board[x2][y2]) {
            return false;
        }

        // Check if there's a path
        return has_path(pos1, pos2);
    }

    void remove_icons(const std::pair<int, int>& pos1, const std::pair<int, int>& pos2) {
        int x1 = pos1.first, y1 = pos1.second;
        int x2 = pos2.first, y2 = pos2.second;
        board[x1][y1] = ' ';
        board[x2][y2] = ' ';
    }

    bool is_game_over() {
        for (const auto& row : board) {
            for (char cell : row) {
                if (cell != ' ') {
                    return false;
                }
            }
        }
        return true;
    }
};