#include <vector>
#include <optional>

class TicTacToe {
public:
    std::vector<std::vector<char>> board;
    char current_player;

    // Initialize a 3-row x N-column game board with empty spaces; current player defaults to 'X'.
    explicit TicTacToe(int N = 3)
        : board(3, std::vector<char>(N, ' ')), current_player('X') {}

    // Place the current player's mark at (row, col) if empty, then switch players.
    // Returns true on success, false if the cell is occupied.
    // Throws std::out_of_range on invalid indices (mirrors Python IndexError).
    bool make_move(int row, int col) {
        if (board.at(row).at(col) == ' ') {
            board[row][col] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        } else {
            return false;
        }
    }

    // Check rows, columns, and diagonals for a winner.
    // Returns the winner's mark ('X' or 'O'), or std::nullopt (Python None) if none.
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

    // Return true if no empty cells remain on the board.
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