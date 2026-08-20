#include <optional>
#include <vector>

class TicTacToe {
public:
    // 3 rows x N columns; ' ' marks an empty cell. Current player starts as 'X'.
    std::vector<std::vector<char>> board;
    char current_player;

    // Initialize the board with 3 rows and N columns of empty cells.
    // (Python's range(N) yields an empty sequence for N <= 0, hence the clamp.)
    explicit TicTacToe(int N = 3)
        : board(3, std::vector<char>(N > 0 ? N : 0, ' ')),
          current_player('X') {}

    // Place the current player's mark at (row, col) and switch players.
    // Returns true if the move was made, false if the cell was already occupied.
    // Out-of-range indices throw std::out_of_range (mirrors Python's IndexError).
    bool make_move(int row, int col) {
        if (board.at(row).at(col) == ' ') {
            board[row][col] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    // Check all rows, columns and both diagonals for a winner.
    // Returns the winner's mark ('X' or 'O'), or std::nullopt if there is no winner yet.
    std::optional<char> check_winner() const {
        for (const auto& row : board) {
            if (row.at(0) == row.at(1) && row.at(1) == row.at(2) && row.at(2) != ' ') {
                return row[0];
            }
        }
        for (int col = 0; col < 3; ++col) {
            if (board.at(0).at(col) == board.at(1).at(col) &&
                board.at(1).at(col) == board.at(2).at(col) &&
                board.at(2).at(col) != ' ') {
                return board[0][col];
            }
        }
        if (board.at(0).at(0) == board.at(1).at(1) &&
            board.at(1).at(1) == board.at(2).at(2) &&
            board.at(2).at(2) != ' ') {
            return board[0][0];
        }
        if (board.at(0).at(2) == board.at(1).at(1) &&
            board.at(1).at(1) == board.at(2).at(0) &&
            board.at(2).at(0) != ' ') {
            return board[0][2];
        }
        return std::nullopt;
    }

    // Return true if the board is completely filled (no empty cells).
    bool is_board_full() const {
        for (const auto& row : board) {
            for (char cell : row) {
                if (cell == ' ') {
                    return false;
                }
            }
        }
        return true;
    }
};