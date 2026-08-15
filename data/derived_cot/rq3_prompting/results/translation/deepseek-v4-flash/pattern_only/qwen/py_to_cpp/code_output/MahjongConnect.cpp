#include <vector>
#include <string>
#include <random>
#include <set>
#include <utility>
#include <stdexcept>

class MahjongConnect {
public:
    std::vector<int> BOARD_SIZE;
    std::vector<std::string> ICONS;
    std::vector<std::vector<std::string>> board;

    MahjongConnect(std::vector<int> BOARD_SIZE, std::vector<std::string> ICONS)
        : BOARD_SIZE(std::move(BOARD_SIZE)), ICONS(std::move(ICONS)), board(create_board()) {}

    std::vector<std::vector<std::string>> create_board() {
        int rows = BOARD_SIZE.at(0) > 0 ? BOARD_SIZE.at(0) : 0;
        int cols = BOARD_SIZE.at(1) > 0 ? BOARD_SIZE.at(1) : 0;
        std::vector<std::vector<std::string>> b(rows, std::vector<std::string>(cols));

        if (ICONS.empty()) {
            if (rows > 0 && cols > 0) {
                throw std::out_of_range("choice() from an empty sequence");
            }
            return b;
        }

        std::uniform_int_distribution<size_t> dist(0, ICONS.size() - 1);
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                b[i][j] = ICONS[dist(rng())];
            }
        }
        return b;
    }

    bool is_valid_move(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        int x1 = pos1.first, y1 = pos1.second;
        int x2 = pos2.first, y2 = pos2.second;

        if (!(0 <= x1 && x1 < BOARD_SIZE.at(0) && 0 <= y1 && y1 < BOARD_SIZE.at(1) &&
              0 <= x2 && x2 < BOARD_SIZE.at(0) && 0 <= y2 && y2 < BOARD_SIZE.at(1))) {
            return false;
        }

        if (pos1 == pos2) return false;

        if (icon_at(x1, y1) != icon_at(x2, y2)) return false;

        if (!has_path(pos1, pos2)) return false;

        return true;
    }

    bool has_path(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        std::set<std::pair<int, int>> visited;
        std::vector<std::pair<int, int>> stack;
        stack.push_back(pos1);

        while (!stack.empty()) {
            auto current_pos = stack.back();
            stack.pop_back();

            if (current_pos == pos2) return true;

            if (visited.find(current_pos) != visited.end()) continue;

            visited.insert(current_pos);
            int x = current_pos.first;
            int y = current_pos.second;

            int dxs[] = {0, 0, 1, -1};
            int dys[] = {1, -1, 0, 0};

            for (int i = 0; i < 4; ++i) {
                int new_x = x + dxs[i];
                int new_y = y + dys[i];

                if (0 <= new_x && new_x < BOARD_SIZE.at(0) && 0 <= new_y && new_y < BOARD_SIZE.at(1)) {
                    if (visited.find({new_x, new_y}) == visited.end()) {
                        const std::string& neighbor_icon = icon_at(new_x, new_y);
                        const std::string& current_icon = icon_at(x, y);
                        if (neighbor_icon == current_icon) {
                            stack.push_back({new_x, new_y});
                        }
                    }
                }
            }
        }

        return false;
    }

    void remove_icons(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        icon_at(pos1.first, pos1.second) = " ";
        icon_at(pos2.first, pos2.second) = " ";
    }

    bool is_game_over() {
        for (const auto& row : board) {
            for (const auto& icon : row) {
                if (icon != " ") return false;
            }
        }
        return true;
    }

private:
    std::string& icon_at(int x, int y) {
        if (x < 0) x += static_cast<int>(board.size());
        if (x < 0) throw std::out_of_range("board index out of range");

        if (y < 0) y += static_cast<int>(board.at(x).size());
        if (y < 0) throw std::out_of_range("board index out of range");

        return board.at(x).at(y);
    }

    static std::mt19937& rng() {
        static std::mt19937 rng{std::random_device{}()};
        return rng;
    }
};