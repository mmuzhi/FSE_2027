#include <vector>
#include <string>
#include <optional>
#include <algorithm>

class TicTacToe {
private:
    std::vector<std::vector<char>> board;
    char current_player;

public:
    TicTacToe(int N = 3) : board(3, std::vector<char>(N, ' ')), current_player('X') {}

    bool make_move(int row, int col) {
        if (board.at(row).at(col) == ' ') {
            board.at(row).at(col) = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        } else {
            return false;
        }
    }

    std::optional<std::string> check_winner() {
        for (const auto& row : board) {
            if (row.at(0) == row.at(1) && row.at(1) == row.at(2) && row.at(0) != ' ') {
                return std::string(1, row.at(0));
            }
        }
        for (int col = 0; col < 3; ++col) {
            if (board.at(0).at(col) == board.at(1).at(col) && board.at(1).at(col) == board.at(2).at(col) && board.at(0).at(col) != ' ') {
                return std::string(1, board.at(0).at(col));
            }
        }
        if (board.at(0).at(0) == board.at(1).at(1) && board.at(1).at(1) == board.at(2).at(2) && board.at(0).at(0) != ' ') {
            return std::string(1, board.at(0).at(0));
        }
        if (board.at(0).at(2) == board.at(1).at(1) && board.at(1).at(1) == board.at(2).at(0) && board.at(0).at(2) != ' ') {
            return std::string(1, board.at(0).at(2));
        }
        return std::nullopt;
    }

    bool is_board_full() {
        for (const auto& row : board) {
            if (std::find(row.begin(), row.end(), ' ') != row.end()) {
                return false;
            }
        }
        return true;
    }
};