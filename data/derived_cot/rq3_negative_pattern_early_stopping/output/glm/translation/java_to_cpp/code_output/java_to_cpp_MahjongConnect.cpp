#include <iostream>
#include <vector>
#include <string>
#include <random>

class MahjongConnect {
public:
    std::vector<int> BOARD_SIZE;
    std::vector<std::string> ICONS;
    std::vector<std::vector<std::string>> board;

    MahjongConnect(std::vector<int> BOARD_SIZE, std::vector<std::string> ICONS) {
        this->BOARD_SIZE = std::move(BOARD_SIZE);
        this->ICONS = std::move(ICONS);
        this->board = createBoard();
    }

    std::vector<std::vector<std::string>> createBoard() {
        std::vector<std::vector<std::string>> board(BOARD_SIZE[0], std::vector<std::string>(BOARD_SIZE[1]));
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<int> distrib(0, static_cast<int>(ICONS.size()) - 1);

        for (int i = 0; i < BOARD_SIZE[0]; i++) {
            for (int j = 0; j < BOARD_SIZE[1]; j++) {
                board[i][j] = ICONS[distrib(gen)];
            }
        }
        return board;
    }

    bool isValidMove(const std::vector<int>& pos1, const std::vector<int>& pos2) {
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

        return hasPath(pos1, pos2);
    }

private:
    bool isValidPosition(int x, int y) {
        return x >= 0 && x < BOARD_SIZE[0] && y >= 0 && y < BOARD_SIZE[1];
    }

public:
    bool hasPath(const std::vector<int>& pos1, const std::vector<int>& pos2) {
        int x1 = pos1[0], y1 = pos1[1];
        int x2 = pos2[0], y2 = pos2[1];

        if (!isValidPosition(x1, y1) || !isValidPosition(x2, y2)) {
            return false;
        }

        std::vector<std::vector<bool>> visited(BOARD_SIZE[0], std::vector<bool>(BOARD_SIZE[1], false));
        return dfs(x1, y1, pos2, visited);
    }

private:
    bool dfs(int x, int y, const std::vector<int>& target, std::vector<std::vector<bool>>& visited) {
        if (x == target[0] && y == target[1]) {
            return true;
        }

        if (visited[x][y]) {
            return false;
        }

        visited[x][y] = true;

        int directions[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
        for (auto& dir : directions) {
            int newX = x + dir[0];
            int newY = y + dir[1];
            if (isValidPosition(newX, newY) && !visited[newX][newY] && board[newX][newY] == board[x][y]) {
                if (dfs(newX, newY, target, visited)) {
                    return true;
                }
            }
        }

        return false;
    }

public:
    void removeIcons(const std::vector<int>& pos1, const std::vector<int>& pos2) {
        board[pos1[0]][pos1[1]] = " ";
        board[pos2[0]][pos2[1]] = " ";
    }

    bool isGameOver() {
        for (int i = 0; i < BOARD_SIZE[0]; i++) {
            for (int j = 0; j < BOARD_SIZE[1]; j++) {
                if (board[i][j] != " ") {
                    return false;
                }
            }
        }
        return true;
    }
};

int main() {
    std::vector<int> boardSize = {4, 4};
    std::vector<std::string> icons = {"a", "b", "c"};

    MahjongConnect mc(boardSize, icons);
    std::cout << std::boolalpha << mc.isValidMove({0, 0}, {1, 0}) << std::endl;
    mc.removeIcons({0, 0}, {1, 0});
    std::cout << std::boolalpha << mc.isGameOver() << std::endl;
    return 0;
}