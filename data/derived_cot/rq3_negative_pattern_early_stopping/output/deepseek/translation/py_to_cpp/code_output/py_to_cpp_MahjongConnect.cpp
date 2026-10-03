#include <vector>
#include <string>
#include <random>
#include <stack>
#include <utility>
#include <algorithm>

class MahjongConnect {
public:
    std::vector<int> BOARD_SIZE;
    std::vector<char> ICONS;
    std::vector<std::vector<char>> board;

    MahjongConnect(std::vector<int> BOARD_SIZE, std::vector<std::string> ICONS)
        : BOARD_SIZE(BOARD_SIZE), ICONS(ICONS.begin(), ICONS.end()) {
        board = create_board();
    }

    std::vector<std::vector<char>> create_board() {
        std::vector<std::vector<char>> new_board(BOARD_SIZE[0],
            std::vector<char>(BOARD_SIZE[1]));
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(0, ICONS.size() - 1);
        for (int i = 0; i < BOARD_SIZE[0]; ++i) {
            for (int j = 0; j < BOARD_SIZE[1]; ++j) {
                new_board[i][j] = ICONS[dis(gen)];
            }
        }
        return new_board;
    }

    bool is_valid_move(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        int x1 = pos1.first, y1 = pos1.second;
        int x2 = pos2.first, y2 = pos2.second;

        if (!(0 <= x1 && x1 < BOARD_SIZE[0] && 0 <= y1 && y1 < BOARD_SIZE[1] &&
              0 <= x2 && x2 < BOARD_SIZE[0] && 0 <= y2 && y2 < BOARD_SIZE[1])) {
            return false;
        }
        if (pos1 == pos2) return false;
        if (board[x1][y1] != board[x2][y2]) return false;
        if (!has_path(pos1, pos2)) return false;
        return true;
    }

    bool has_path(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        std::vector<std::vector<bool>> visited(BOARD_SIZE[0], std::vector<bool>(BOARD_SIZE[1], false));
        std::stack<std::pair<int, int>> stk;
        stk.push(pos1);

        while (!stk.empty()) {
            auto cur = stk.top(); stk.pop();
            if (cur == pos2) return true;
            if (visited[cur.first][cur.second]) continue;
            visited[cur.first][cur.second] = true;

            int dx[] = {0, 0, 1, -1};
            int dy[] = {1, -1, 0, 0};
            for (int d = 0; d < 4; ++d) {
                int nx = cur.first + dx[d];
                int ny = cur.second + dy[d];
                if (nx >= 0 && nx < BOARD_SIZE[0] && ny >= 0 && ny < BOARD_SIZE[1] &&
                    !visited[nx][ny] && board[nx][ny] == board[cur.first][cur.second]) {
                    stk.push({nx, ny});
                }
            }
        }
        return false;
    }

    void remove_icons(std::pair<int, int> pos1, std::pair<int, int> pos2) {
        board[pos1.first][pos1.second] = ' ';
        board[pos2.first][pos2.second] = ' ';
    }

    bool is_game_over() {
        for (const auto& row : board) {
            for (char c : row) {
                if (c != ' ') return false;
            }
        }
        return true;
    }
};