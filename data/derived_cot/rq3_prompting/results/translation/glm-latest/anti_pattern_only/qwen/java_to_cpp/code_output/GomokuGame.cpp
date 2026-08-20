#include <iostream>
#include <optional>
#include <stdexcept>
#include <string>
#include <vector>

class GomokuGame {
private:
    int boardSize;
    std::vector<std::vector<char>> board;
    char currentPlayer;

    bool checkFiveInARow(int row, int col, const int (&direction)[2]) {
        int dx = direction[0];
        int dy = direction[1];
        int count = 1;
        char symbol = board[row][col];
        for (int i = 1; i < 5; i++) {
            int newRow = row + dx * i;
            int newCol = col + dy * i;
            if (newRow < 0 || newRow >= boardSize || newCol < 0 || newCol >= boardSize) {
                break;
            }
            if (board[newRow][newCol] != symbol) {
                break;
            }
            count++;
        }
        for (int i = 1; i < 5; i++) {
            int newRow = row - dx * i;
            int newCol = col - dy * i;
            if (newRow < 0 || newRow >= boardSize || newCol < 0 || newCol >= boardSize) {
                break;
            }
            if (board[newRow][newCol] != symbol) {
                break;
            }
            count++;
        }
        return count >= 5;
    }

public:
    explicit GomokuGame(int boardSize)
        : boardSize(boardSize),
          board(boardSize, std::vector<char>(boardSize, ' ')),
          currentPlayer('X') {}

    bool makeMove(int row, int col) {
        // Java throws ArrayIndexOutOfBoundsException on out-of-range access;
        // mirror that with an exception here.
        if (row < 0 || row >= boardSize || col < 0 || col >= boardSize) {
            throw std::out_of_range("Array index out of bounds: row=" +
                                    std::to_string(row) + ", col=" + std::to_string(col));
        }
        if (board[row][col] == ' ') {
            board[row][col] = currentPlayer;
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    std::optional<char> checkWinner() {
        static const int directions[4][2] = {{0, 1}, {1, 0}, {1, 1}, {1, -1}};
        for (int row = 0; row < boardSize; row++) {
            for (int col = 0; col < boardSize; col++) {
                if (board[row][col] != ' ') {
                    for (const auto& direction : directions) {
                        if (checkFiveInARow(row, col, direction)) {
                            return board[row][col];
                        }
                    }
                }
            }
        }
        return std::nullopt;
    }
};

int main() {
    GomokuGame gomokuGame(10);
    const int moves[9][2] = {{5, 5}, {0, 0}, {5, 4}, {0, 1}, {5, 3}, {0, 2}, {5, 2}, {0, 3}, {5, 1}};
    for (const auto& move : moves) {
        gomokuGame.makeMove(move[0], move[1]);
    }
    std::optional<char> winner = gomokuGame.checkWinner();
    if (winner.has_value()) {
        std::cout << *winner << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }
    return 0;
}