#include <vector>
#include <optional>
#include <algorithm>

class TicTacToe {
public:
    // Initialize a game board (always 3 rows, N columns) with all empty
    // spaces and the current player's mark, default 'X'.
    explicit TicTacToe(int N = 3)
        : board(3, std::vector<char>(static_cast<size_t>(N), ' ')),
          current_player('X') {}

    // Place the current player's mark at the specified position on the
    // board and switch the mark. Returns whether the move succeeded.
    bool make_move(int row, int col) {
        if (board.at(static_cast<size_t>(row)).at(static_cast<size_t>(col)) == ' ') {
            board[static_cast<size_t>(row)][static_cast<size_t>(col)] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        } else {
            return false;
        }
    }

    // Check rows, columns and diagonals for a winner.
    // Returns the winner's mark ('X' or 'O'), or std::nullopt if none.
    std::optional<char> check_winner() const {
        for (const auto& row : board) {
            if (row.at(0) == row.at(1) && row.at(1) == row.at(2) && row.at(2) != ' ') {
                return row[0];
            }
        }
        for (size_t col = 0; col < 3; ++col) {
            if (board[0].at(col) == board[1].at(col) &&
                board[1].at(col) == board[2].at(col) &&
                board[2][col] != ' ') {
                return board[0][col];
            }
        }
        if (board[0].at(0) == board[1].at(1) && board[1].at(1) == board[2].at(2) &&
            board[2][2] != ' ') {
            return board[0][0];
        }
        if (board[0].at(2) == board[1].at(1) && board[1].at(1) == board[2].at(0) &&
            board[2][0] != ' ') {
            return board[0][2];
        }
        return std::nullopt;
    }

    // Check if the game board is completely filled.
    bool is_board_full() const {
        for (const auto& row : board) {
            if (std::find(row.begin(), row.end(), ' ') != row.end()) {
                return false;
            }
        }
        return true;
    }

private:
    std::vector<std::vector<char>> board;
    char current_player;
};