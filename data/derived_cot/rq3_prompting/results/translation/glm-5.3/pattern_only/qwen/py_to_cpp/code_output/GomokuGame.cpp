#include <optional>
#include <stdexcept>
#include <utility>
#include <vector>

// This class is an implementation of a Gomoku game, supporting making moves,
// checking for a winner, and checking if there are five consecutive symbols on the board.
class GomokuGame {
public:
    // Initializes the game with a given board size.
    // The board is filled with empty spaces and the current player starts as 'X'.
    explicit GomokuGame(int board_size)
        : board_size(board_size),
          board(static_cast<size_t>(board_size > 0 ? board_size : 0),
                std::vector<char>(static_cast<size_t>(board_size > 0 ? board_size : 0), ' ')),
          current_player('X') {}

    // Makes a move at the given row and column.
    // If the move is valid, places the current player's symbol on the board and
    // switches the current player ('X' -> 'O', 'O' -> 'X').
    // Returns true if the move is valid, false otherwise.
    // Python-style indexing: negative indices wrap; out-of-range throws (IndexError analog).
    bool make_move(int row, int col) {
        if (at(row, col) == ' ') {
            at(row, col) = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    // Checks for a winner by looking for five in a row in all directions
    // (horizontal, vertical, diagonal).
    // Returns the winning symbol ('X' or 'O') if there is a winner, std::nullopt otherwise.
    std::optional<char> check_winner() {
        static const std::pair<int, int> directions[] = {
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
        return std::nullopt;
    }

    // Checks for five consecutive symbols of the same player starting from a given
    // cell in a given direction (dx, dy). Row and col are advanced by multiples of
    // dx and dy respectively.
    // Returns true if there are five consecutive symbols, false otherwise.
    bool _check_five_in_a_row(int row, int col, std::pair<int, int> direction) {
        int dx = direction.first;
        int dy = direction.second;
        int count = 1;
        char symbol = at(row, col);
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
            count += 1;
        }
        return count == 5;
    }

private:
    int board_size;
    std::vector<std::vector<char>> board;
    char current_player;

    // Python list-indexing semantics: negative index wraps (idx + size);
    // still out of range -> throw (mirrors Python IndexError).
    char& at(int row, int col) {
        int r = wrap_index(row, board_size);
        int c = wrap_index(col, board_size);
        return board[static_cast<size_t>(r)][static_cast<size_t>(c)];
    }

    static int wrap_index(int idx, int size) {
        if (idx < 0) {
            idx += size;
        }
        if (idx < 0 || idx >= size) {
            throw std::out_of_range("index out of range");
        }
        return idx;
    }
};