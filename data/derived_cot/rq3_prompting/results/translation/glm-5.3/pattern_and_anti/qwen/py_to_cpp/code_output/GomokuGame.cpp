#include <vector>
#include <utility>
#include <stdexcept>

class GomokuGame {
public:
    GomokuGame(int board_size)
        : board_size(board_size), current_player('X') {
        if (board_size > 0) {
            board.assign(static_cast<size_t>(board_size),
                         std::vector<char>(static_cast<size_t>(board_size), ' '));
        }
    }

    bool make_move(int row, int col) {
        // Mirrors Python indexing: negative indices wrap; out of range raises IndexError.
        int r = py_index(row);
        int c = py_index(col);
        if (board[r][c] == ' ') {
            board[r][c] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    // Returns 'X' or 'O' if there is a winner, '\0' (None) otherwise.
    char check_winner() {
        static const std::pair<int, int> directions[4] = {
            {0, 1}, {1, 0}, {1, 1}, {1, -1}};
        for (int row = 0; row < board_size; ++row) {
            for (int col = 0; col < board_size; ++col) {
                if (board[row][col] != ' ') {
                    for (const auto& direction : directions) {
                        if (_check_five_in_a_row(row, col, direction)) {
                            return board[row][col];
                        }
                    }
                }
            }
        }
        return '\0';
    }

    bool _check_five_in_a_row(int row, int col, std::pair<int, int> direction) {
        int dx = direction.first;
        int dy = direction.second;
        int count = 1;
        // Mirrors Python indexing for the starting cell (negative wrap / IndexError).
        char symbol = board[py_index(row)][py_index(col)];
        for (int i = 1; i < 5; ++i) {
            int new_row = row + dx * i;
            int new_col = col + dy * i;
            if (!(0 <= new_row && new_row < board_size &&
                  0 <= new_col && new_col < board_size)) {
                return false;
            }
            if (board[new_row][new_col] != symbol) {
                return false;
            }
            ++count;
        }
        return count == 5;
    }

private:
    int board_size;
    std::vector<std::vector<char>> board;
    char current_player;

    // Python-style index normalization: negative indices count from the end,
    // anything still out of range raises (Python IndexError equivalent).
    int py_index(int idx) const {
        int i = idx;
        if (i < 0) i += board_size;
        if (i < 0 || i >= board_size) {
            throw std::out_of_range("index out of range");
        }
        return i;
    }
};