#include <iostream>
#include <vector>

class GomokuGame {
    int boardSize;
    std::vector<std::vector<char>> board;
    char currentPlayer;

public:
    GomokuGame(int boardSize) : boardSize(boardSize), currentPlayer('X') {
        board.resize(boardSize, std::vector<char>(boardSize, ' '));
    }

    bool makeMove(int row, int col) {
        if (row < 0 || row >= boardSize || col < 0 || col >= boardSize) {
            return false;
        }
        if (board[row][col] == ' ') {
            board[row][col] = currentPlayer;
            currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    char checkWinner() {
        int directions[4][2] = {{0, 1}, {1, 0}, {1, 1}, {1, -1}};
        for (int row = 0; row < boardSize; ++row) {
            for (int col = 0; col < boardSize; ++col) {
                if (board[row][col] != ' ') {
                    for (const auto& dir : directions) {
                        if (checkFiveInARow(row, col, dir[0], dir[1])) {
                            return board[row][col];
                        }
                    }
                }
            }
        }
        return '\0';
    }

private:
    bool checkFiveInARow(int row, int col, int dx, int dy) {
        int count = 1;
        char symbol = board[row][col];
        for (int i = 1; i < 5; ++i) {
            int newRow = row + dx * i;
            int newCol = col + dy * i;
            if (newRow < 0 || newRow >= boardSize || newCol < 0 || newCol >= boardSize) break;
            if (board[newRow][newCol] != symbol) break;
            ++count;
        }
        for (int i = 1; i < 5; ++i) {
            int newRow = row - dx * i;
            int newCol = col - dy * i;
            if (newRow < 0 || newRow >= boardSize || newCol < 0 || newCol >= boardSize) break;
            if (board[newRow][newCol] != symbol) break;
            ++count;
        }
        return count >= 5;
    }
};

int main() {
    GomokuGame gomokuGame(10);
    int moves[][2] = {{5, 5}, {0, 0}, {5, 4}, {0, 1}, {5, 3}, {0, 2}, {5, 2}, {0, 3}, {5, 1}};
    for (const auto& move : moves) {
        gomokuGame.makeMove(move[0], move[1]);
    }
    std::cout << gomokuGame.checkWinner() << std::endl;
    return 0;
}