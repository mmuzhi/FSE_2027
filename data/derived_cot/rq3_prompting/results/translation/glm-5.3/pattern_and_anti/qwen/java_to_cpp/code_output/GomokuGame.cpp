#include <iostream>
#include <vector>
#include <optional>

class GomokuGame {
private:
    int boardSize;
    std::vector<std::vector<char>> board;
    char currentPlayer;

public:
    explicit GomokuGame(int boardSize)
        : boardSize(boardSize),
          board(boardSize, std::vector<char>(boardSize, ' ')),
          currentPlayer('X') {}

    bool makeMove(int row, int col) {
        if (this->board.at(row).at(col) == ' ') {
            this->board[row][col] = this->currentPlayer;
            this->currentPlayer = (this->currentPlayer == 'X') ? 'O' : 'X';
            return true;
        }
        return false;
    }

    std::optional<char> checkWinner() {
        static const int directions[4][2] = {{0, 1}, {1, 0}, {1, 1}, {1, -1}};
        for (int row = 0; row < this->boardSize; row++) {
            for (int col = 0; col < this->boardSize; col++) {
                if (this->board[row][col] != ' ') {
                    for (const auto& direction : directions) {
                        if (checkFiveInARow(row, col, direction)) {
                            return this->board[row][col];
                        }
                    }
                }
            }
        }
        return std::nullopt;
    }

    bool checkFiveInARow(int row, int col, const int (&direction)[2]) {
        int dx = direction[0];
        int dy = direction[1];
        int count = 1;
        char symbol = this->board[row][col];
        for (int i = 1; i < 5; i++) {
            int newRow = row + dx * i;
            int newCol = col + dy * i;
            if (newRow < 0 || newRow >= this->boardSize || newCol < 0 || newCol >= this->boardSize) {
                break;
            }
            if (this->board[newRow][newCol] != symbol) {
                break;
            }
            count++;
        }
        for (int i = 1; i < 5; i++) {
            int newRow = row - dx * i;
            int newCol = col - dy * i;
            if (newRow < 0 || newRow >= this->boardSize || newCol < 0 || newCol >= this->boardSize) {
                break;
            }
            if (this->board[newRow][newCol] != symbol) {
                break;
            }
            count++;
        }
        return count >= 5;
    }
};

int main() {
    GomokuGame gomokuGame(10);
    static const int moves[9][2] = {{5, 5}, {0, 0}, {5, 4}, {0, 1}, {5, 3}, {0, 2}, {5, 2}, {0, 3}, {5, 1}};
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