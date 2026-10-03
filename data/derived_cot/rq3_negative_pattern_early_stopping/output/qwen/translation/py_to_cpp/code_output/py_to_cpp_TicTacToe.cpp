#include <vector>
#include <string>

class TicTacToe {
private:
    std::vector<std::vector<char>> board;
    char current_player;

public:
    TicTacToe(int N=3) {
        board.resize(3, std::vector<char>(N, ' '));
        current_player = 'X';
    }

    bool make_move(int row, int col) {
        if (board[row][col] == ' ') {
            board[row][col] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    char check_winner() {
        // Check rows
        for (int i = 0; i < 3; i++) {
            if (board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != ' ') {
                return board[i][0];
            }
        }

        // Check columns
        for (int j = 0; j < 3; j++) {
            if (board[0][j] == board[1][j] && board[1][j] == board[2][j] && board[0][j] != ' ') {
                return board[0][j];
            }
        }

        // Check diagonals
        if (board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != ' ') {
            return board[0][0];
        }

        if (board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != ' ') {
            return board[0][2];
        }

        return ' '; // Return space to indicate no winner (as in None in Python, but space is not a valid winner)
    }

    bool is_board_full() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < board[i].size(); j++) {
                if (board[i][j] == ' ') {
                    return false;
                }
            }
        }
        return true;
    }
};