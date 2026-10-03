#include <iostream>
#include <vector>
#include <optional>

class GomokuGame {
private:
    int boardSize;
    std::vector<std::vector<char>> board;
    char currentPlayer;

public:
    GomokuGame(int boardSize) : boardSize(boardSize), board(boardSize, std::vector<char>(boardSize, ' ')), currentPlayer('X') {}

    bool makeMove(int row, int col) {
        if (board[row][col] == ' ') {
            board[row][col] = currentPlayer;
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    std::optional<char> checkWinner() {
        int directions[4][2] = {{0, 1}, {1, 0}, {1, 1}, {1, -1}};
        for (int row = 0; row < boardSize; ++row) {
            for (int col = 0; col < boardSize; ++col) {
                if (board[row][col] != ' ') {
                    for (auto& dir : directions) {
                        if (checkFiveInARow(row, col, dir)) {
                            return board[row][col];
                        }
                    }
                }
            }
        }
        return std::nullopt;
    }

private:
    bool checkFiveInARow(int row, int col, int direction[2]) {
        int dx = direction[0];
        int dy = direction[1];
        int count = 1;
        char symbol = board[row][col];
        for (int i = 1; i < 5; ++i) {
            int newRow = row + dx * i;
            int newCol = col + dy * i;
            if (newRow < 0 || newRow >= boardSize || newCol < 0 || newCol >= boardSize) {
                break;
            }
            if (board[newRow][newCol] != symbol) {
                break;
            }
            ++count;
        }
        for (int i = 1; i < 5; ++i) {
            int newRow = row - dx * i;
            int newCol = col - dy * i;
            if (newRow < 0 || newRow >= boardSize || newCol < 0 || newCol >= boardSize) {
                break;
            }
            if (board[newRow][newCol] != symbol) {
                break;
            }
            ++count;
        }
        return count >= 5;
    }
};

int main() {
    GomokuGame gomokuGame(10);
    int moves[][2] = {{5, 5}, {0, 0}, {5, 4}, {0, 1}, {5, 3}, {0, 2}, {5, 2}, {0, 3}, {5, 1}};
    for (auto& move : moves) {
        gomokuGame.makeMove(move[0], move[1]);
    }
    auto winner = gomokuGame.checkWinner();
    if (winner.has_value()) {
        std::cout << winner.value() << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }
    return 0;
}