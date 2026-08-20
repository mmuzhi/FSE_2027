#include <cstddef>
#include <vector>

class PushBoxGame {
private:
    std::vector<std::vector<char>> map;
    int playerRow;
    int playerCol;
    std::vector<std::vector<int>> targets;
    std::vector<std::vector<int>> boxes;
    int targetCount;
    bool gameOver; // Java field "isGameOver" (renamed: clashes with the method name in C++)

    void initGame() {
        for (std::size_t row = 0; row < map.size(); row++) {
            for (std::size_t col = 0; col < map[row].size(); col++) {
                if (map[row][col] == 'O') {
                    this->playerRow = static_cast<int>(row);
                    this->playerCol = static_cast<int>(col);
                } else if (map[row][col] == 'G') {
                    this->targets.push_back(std::vector<int>{static_cast<int>(row), static_cast<int>(col)});
                    this->targetCount++;
                } else if (map[row][col] == 'X') {
                    this->boxes.push_back(std::vector<int>{static_cast<int>(row), static_cast<int>(col)});
                }
            }
        }
    }

    bool isValidMove(int row, int col) {
        return row >= 0 && row < static_cast<int>(map.size())
            && col >= 0 && col < static_cast<int>(map[row].size())
            && map[row][col] != '#';
    }

    bool isBoxAt(int row, int col) {
        for (const std::vector<int>& box : boxes) {
            if (box == std::vector<int>{row, col}) {
                return true;
            }
        }
        return false;
    }

    std::vector<int> getBoxPosition(int row, int col) {
        for (const std::vector<int>& box : boxes) {
            if (box == std::vector<int>{row, col}) {
                return box;
            }
        }
        // Java returns null here; a {-1,-1} sentinel never matches a real box,
        // so the caller (moveBox) performs no move, exactly like the Java version.
        return std::vector<int>{-1, -1};
    }

    void moveBox(const std::vector<int>& boxPosition, int newRow, int newCol) {
        for (std::vector<int>& box : boxes) {
            if (box == boxPosition) {
                box = std::vector<int>{newRow, newCol};
                break;
            }
        }
    }

public:
    PushBoxGame(const std::vector<std::vector<char>>& map)
        : map(map),
          playerRow(0),
          playerCol(0),
          targetCount(0),
          gameOver(false) {
        initGame();
    }

    bool checkWin() {
        int boxOnTargetCount = 0;
        for (const std::vector<int>& box : boxes) {
            for (const std::vector<int>& target : targets) {
                if (box == target) {
                    boxOnTargetCount++;
                }
            }
        }
        gameOver = (boxOnTargetCount == targetCount);
        return gameOver;
    }

    bool move(char direction) {
        int newPlayerRow = playerRow;
        int newPlayerCol = playerCol;

        if (direction == 'w') {
            newPlayerRow -= 1;
        } else if (direction == 's') {
            newPlayerRow += 1;
        } else if (direction == 'a') {
            newPlayerCol -= 1;
        } else if (direction == 'd') {
            newPlayerCol += 1;
        }

        if (isValidMove(newPlayerRow, newPlayerCol)) {
            if (isBoxAt(newPlayerRow, newPlayerCol)) {
                std::vector<int> boxPosition = getBoxPosition(newPlayerRow, newPlayerCol);
                int newBoxRow = newPlayerRow + (newPlayerRow - playerRow);
                int newBoxCol = newPlayerCol + (newPlayerCol - playerCol);

                if (isValidMove(newBoxRow, newBoxCol) && !isBoxAt(newBoxRow, newBoxCol)) {
                    moveBox(boxPosition, newBoxRow, newBoxCol);
                    playerRow = newPlayerRow;
                    playerCol = newPlayerCol;
                }
            } else {
                playerRow = newPlayerRow;
                playerCol = newPlayerCol;
            }
        }

        return checkWin();
    }

    bool isGameOver() const {
        return gameOver;
    }

    int getPlayerCol() const {
        return playerCol;
    }

    int getPlayerRow() const {
        return playerRow;
    }

    std::vector<std::vector<int>> getTargets() const {
        return targets;
    }

    int getTargetCount() const {
        return targetCount;
    }

    // Java returns the internal array reference (not a copy), so a reference is
    // returned here to keep the same aliasing/mutation semantics.
    std::vector<std::vector<char>>& getMap() {
        return map;
    }

    const std::vector<std::vector<char>>& getMap() const {
        return map;
    }

    std::vector<std::vector<int>> getBoxes() const {
        return boxes;
    }
};