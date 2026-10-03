#include <vector>
#include <iostream>

class TicTacToe {
public:
    TicTacToe(int N = 3) {
        board = std::vector<std::vector<char>>(3, std::vector<char>(N, ' '));
        current_player = 'X';
    }

    bool make_move(int row, int col) {
        if (row >= 0 && row < 3 && col >= 0 && col < static_cast<int>(board[0].size()) && board[row][col] == ' ') {
            board[row][col] = current_player;
            current_player = (current_player == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    char check_winner() {
        // Check rows
        for (int i = 0; i < 3; ++i) {
            if (board[i][0] != ' ' && board[i][0] == board[i][1] && board[i][1] == board[i][2]) {
                return board[i][0];
            }
        }
        // Check columns
        for (int j = 0; j < 3; ++j) {
            if (board[0][j] != ' ' && board[0][j] == board[1][j] && board[1][j] == board[2][j]) {
                return board[0][j];
            }
        }
        // Check main diagonal
        if (board[0][0] != ' ' && board[0][0] == board[1][1] && board[1][1] == board[2][2]) {
            return board[0][0];
        }
        // Check anti-diagonal
        if (board[0][2] != ' ' && board[0][2] == board[1][1] && board[1][1] == board[2][0]) {
            return board[0][2];
        }
        // No winner
        return '\0';
    }

    bool is_board_full() {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < static_cast<int>(board[i].size()); ++j) {
                if (board[i][j] == ' ') {
                    return false;
                }
            }
        }
        return true;
    }

private:
    std::vector<std::vector<char>> board;
    char current_player;
};