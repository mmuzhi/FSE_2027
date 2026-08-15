#include <vector>
#include <optional>

class TicTacToe {
public:
    TicTacToe(int N = 3)
        : board(3, std::vector<char>(N > 0 ? N : 0, ' ')), current_player('X') {}

    bool make_move(int row, int col) {
        if (board.at(row).at(col) == ' ') {
            board.at(row).at(col) = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    std::optional<char> check_winner() {
        for (const auto& row : board) {
            if (row.at(0) == row.at(1) && row.at(1) == row.at(2) && row.at(2) != ' ') {
                return row.at(0);
            }
        }
        for (int col = 0; col < 3; ++col) {
            if (board.at(0).at(col) == board.at(1).at(col) &&
                board.at(1).at(col) == board.at(2).at(col) &&
                board.at(2).at(col) != ' ') {
                return board.at(0).at(col);
            }
        }
        if (board.at(0).at(0) == board.at(1).at(1) &&
            board.at(1).at(1) == board.at(2).at(2) &&
            board.at(2).at(2) != ' ') {
            return board.at(0).at(0);
        }
        if (board.at(0).at(2) == board.at(1).at(1) &&
            board.at(1).at(1) == board.at(2).at(0) &&
            board.at(2).at(0) != ' ') {
            return board.at(0).at(2);
        }
        return std::nullopt;
    }

    bool is_board_full() {
        for (const auto& row : board) {
            for (char c : row) {
                if (c == ' ') {
                    return false;
                }
            }
        }
        return true;
    }

    std::vector<std::vector<char>> board;
    char current_player;
};