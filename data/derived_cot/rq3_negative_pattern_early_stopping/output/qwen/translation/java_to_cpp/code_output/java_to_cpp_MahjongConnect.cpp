#include <vector>
#include <string>
#include <random>
#include <iostream>
#include <algorithm>

class MahjongConnect {
private:
    int boardSize[2];
    std::vector<std::string> icons;
    std::vector<std::vector<std::string>> board;

    // Helper function to check if a position is valid
    bool isValidPosition(int x, int y) {
        return x >= 0 && x < boardSize[0] && y >= 0 && y < boardSize[1];
    }

    // DFS to check if there's a path from (x, y) to target
    bool dfs(int x, int y, const std::vector<int>& target, std::vector<std::vector<bool>>& visited) {
        if (x == target[0] && y == target[1]) {
            return true;
        }

        if (visited[x][y]) {
            return false;
        }

        visited[x][y] = true;

        // Directions: right, left, down, up
        int dx[4] = {0, 0, 1, -1};
        int dy[4] = {1, -1, 0, 0};

        for (int i = 0; i < 4; i++) {
            int newX = x + dx[i];
            int newY = y + dy[i];
            if (isValidPosition(newX, newY) && !visited[newX][newY] && board[x][y] == board[newX][newY]) {
                if (dfs(newX, newY, target, visited)) {
                    return true;
                }
            }
        }

        return false;
    }

public:
    MahjongConnect(int boardSize[2], std::vector<std::string> icons) {
        this->boardSize[0] = boardSize[0];
        this->boardSize[1] = boardSize[1];
        this->icons = icons;
        this->board = createBoard();
    }

    std::vector<std::vector<std::string>> createBoard() {
        std::vector<std::vector<std::string>> board(boardSize[0], std::vector<std::string>(boardSize[1]));
        // Seed the random number generator with current time
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> distrib(0, icons.size()-1);

        for (int i = 0; i < boardSize[0]; i++) {
            for (int j = 0; j < boardSize[1]; j++) {
                board[i][j] = icons[distrib(gen)];
            }
        }
        return board;
    }

    bool isValidMove(std::vector<int> pos1, std::vector<int> pos2) {
        int x1 = pos1[0], y1 = pos1[1];
        int x2 = pos2[0], y2 = pos2[1];

        if (!isValidPosition(x1, y1) || !isValidPosition(x2, y2)) {
            return false;
        }

        if (x1 == x2 && y1 == y2) {
            return false;
        }

        if (board[x1][y1] != board[x2][y2]) {
            return false;
        }

        // Create a visited matrix
        std::vector<std::vector<bool>> visited(boardSize[0], std::vector<bool>(boardSize[1], false));
        return dfs(x1, y1, {x2, y2}, visited);
    }

    void removeIcons(std::vector<int> pos1, std::vector<int> pos2) {
        board[pos1[0]][pos1[1]] = " ";
        board[pos2[0]][pos2[1]] = " ";
    }

    bool isGameOver() {
        for (int i = 0; i < boardSize[0]; i++) {
            for (int j = 0; j < boardSize[1]; j++) {
                if (board[i][j] != " ") {
                    return false;
                }
            }
        }
        return true;
    }
};

// Main function for testing
int main() {
    int boardSize[] = {4, 4};
    std::vector<std::string> icons;
    icons.push_back("a");
    icons.push_back("b");
    icons.push_back("c");

    MahjongConnect mc(boardSize, icons);
    std::vector<int> pos1 = {0, 0};
    std::vector<int> pos2 = {1, 0};

    std::cout << (mc.isValidMove(pos1, pos2) ? "true" : "false") << std::endl;
    mc.removeIcons(pos1, pos2);
    std::cout << (mc.isGameOver() ? "true" : "false") << std::endl;

    return 0;
}