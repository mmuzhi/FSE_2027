#include <cstddef>
#include <optional>
#include <stdexcept>
#include <utility>
#include <vector>

class GomokuGame {
public:
    explicit GomokuGame(int board_size)
        : board_size(board_size), current_player('X') {
        // range(board_size) is empty for non-positive sizes in Python.
        std::size_t n = board_size > 0 ? static_cast<std::size_t>(board_size) : 0;
        board.assign(n, std::vector<char>(n, ' '));
    }

    bool make_move(int row, int col) {
        int r = python_index(row);
        int c = python_index(col);
        if (board[r][c] == ' ') {
            board[r][c] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    std::optional<char> check_winner() {
        static const std::pair<int, int> directions[] = {
            {0, 1}, {1, 0}, {1, 1}, {1, -1}};

        for (int row = 0; row < board_size; ++row) {
            for (int col = 0; col < board_size; ++col) {
                if (board[row][col] != ' ') {
                    for (const std::pair<int, int>& direction : directions) {
                        if (_check_five_in_a_row(row, col, direction)) {
                            return board[row][col];
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
        // Python indexing semantics for the initial cell (negative indices wrap).
        char symbol = board[python_index(row)][python_index(col)];
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

    // Emulates Python list indexing: negative indices count from the end,
    // out-of-range indices raise IndexError.
    int python_index(int idx) const {
        int i = idx;
        if (i < 0) {
            i += board_size;
        }
        if (i < 0 || i >= board_size) {
            throw std::out_of_range("list index out of range");
        }
        return i;
    }
};