#include <array>
#include <optional>
#include <stdexcept>

class TicTacToe {
private:
    std::array<std::array<char, 3>, 3> board;
    char currentPlayer;

public:
    TicTacToe() : currentPlayer('X') {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                board[i][j] = ' ';
            }
        }
    }

    bool makeMove(int row, int col) {
        // Using .at() throws std::out_of_range if indices are invalid, 
        // matching Java's ArrayIndexOutOfBoundsException behavior.
        if (board.at(row).at(col) == ' ') {
            board.at(row).at(col) = currentPlayer;
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
            return true;
        } else {
            return false;
        }
    }

    // std::optional<char> is the C++ equivalent of Java's nullable Character
    std::optional<char> checkWinner() {
        for (int i = 0; i < 3; i++) {
            if (board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != ' ') {
                return board[i][0];
            }
        }
        for (int j = 0; j < 3; j++) {
            if (board[0][j] == board[1][j] && board[1][j] == board[2][j] && board[0][j] != ' ') {
                return board[0][j];
            }
        }
        if (board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != ' ') {
            return board[0][0];
        }
        if (board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != ' ') {
            return board[0][2];
        }
        return std::nullopt; // Equivalent to returning null in Java
    }

    bool isBoardFull() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i][j] == ' ') {
                    return false;
                }
            }
        }
        return true;
    }

    char getCurrentPlayer() {
        return currentPlayer;
    }
};