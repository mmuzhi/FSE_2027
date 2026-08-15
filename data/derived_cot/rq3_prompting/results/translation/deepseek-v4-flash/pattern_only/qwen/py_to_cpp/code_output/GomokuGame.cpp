#include <vector>
#include <optional>
#include <utility>
#include <stdexcept>

class GomokuGame {
public:
    int board_size;
    std::vector<std::vector<char>> board;
    char current_player;

    GomokuGame(int board_size)
        : board_size(board_size),
          board(board_size > 0 ? board_size : 0,
                std::vector<char>(board_size > 0 ? board_size : 0, ' ')),
          current_player('X') {}

    bool make_move(int row, int col) {
        if (cell(row, col) == ' ') {
            cell(row, col) = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    std::optional<char> check_winner() {
        const std::pair<int, int> directions[4] = {
            {0, 1}, {1, 0}, {1, 1}, {1, -1}
        };
        for (int row = 0; row < board_size; ++row) {
            for (int col = 0; col < board_size; ++col) {
                if (cell(row, col) != ' ') {
                    for (const auto& direction : directions) {
                        if (_check_five_in_a_row(row, col, direction)) {
                            return cell(row, col);
                        }
                    }
                }
            }
        }
        return std::nullopt;
    }

    bool _check_five_in_a_row(int row, int col, std::pair<int, int> direction) {
        int dx = direction.first;
        int dy = direction.second;
        int count = 1;
        char symbol = cell(row, col);
        for (int i = 1; i < 5; ++i) {
            int new_row = row + dx * i;
            int new_col = col + dy * i;
            if (!(0 <= new_row && new_row < board_size && 0 <= new_col && new_col < board_size)) {
                return false;
            }
            if (cell(new_row, new_col) != symbol) {
                return false;
            }
            ++count;
        }
        return count == 5;
    }

private:
    char& cell(int row, int col) {
        if (row < 0) row += board.size();
        if (row < 0 || row >= board.size()) {
            throw std::out_of_range("row index out of range");
        }
        if (col < 0) col += board[row].size();
        if (col < 0 || col >= board[row].size()) {
            throw std::out_of_range("col index out of range");
        }
        return board[row][col];
    }
};