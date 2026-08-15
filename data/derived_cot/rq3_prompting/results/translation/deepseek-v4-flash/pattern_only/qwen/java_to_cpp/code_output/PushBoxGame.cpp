#include <vector>
#include <memory>
#include <utility>

class PushBoxGame {
private:
    std::vector<std::vector<char>> map;
    int playerRow;
    int playerCol;
    std::vector<std::shared_ptr<std::pair<int,int>>> targets;
    std::vector<std::shared_ptr<std::pair<int,int>>> boxes;
    int targetCount;
    bool isGameOver;

    void initGame() {
        for (int row = 0; row < (int)map.size(); ++row) {
            for (int col = 0; col < (int)map[row].size(); ++col) {
                if (map[row][col] == 'O') {
                    playerRow = row;
                    playerCol = col;
                } else if (map[row][col] == 'G') {
                    targets.push_back(std::make_shared<std::pair<int,int>>(row, col));
                    ++targetCount;
                } else if (map[row][col] == 'X') {
                    boxes.push_back(std::make_shared<std::pair<int,int>>(row, col));
                }
            }
        }
    }

    bool isValidMove(int row, int col) const {
        return row >= 0 && row < (int)map.size() &&
               col >= 0 && col < (int)map[row].size() &&
               map[row][col] != '#';
    }

    bool isBoxAt(int row, int col) const {
        for (const auto& box : boxes) {
            if (box->first == row && box->second == col) return true;
        }
        return false;
    }

    int findBoxIndex(int row, int col) const {
        for (int i = 0; i < (int)boxes.size(); ++i) {
            if (boxes[i]->first == row && boxes[i]->second == col) return i;
        }
        return -1;
    }

    void moveBox(int index, int newRow, int newCol) {
        boxes[index] = std::make_shared<std::pair<int,int>>(newRow, newCol);
    }

public:
    PushBoxGame(const std::vector<std::vector<char>>& inputMap) {
        map = inputMap;
        playerRow = 0;
        playerCol = 0;
        targetCount = 0;
        isGameOver = false;
        initGame();
    }

    bool checkWin() {
        int boxOnTargetCount = 0;
        for (const auto& box : boxes) {
            for (const auto& target : targets) {
                if (*box == *target) {
                    ++boxOnTargetCount;
                }
            }
        }
        isGameOver = (boxOnTargetCount == targetCount);
        return isGameOver;
    }

    bool move(char direction) {
        int newPlayerRow = playerRow;
        int newPlayerCol = playerCol;

        if (direction == 'w') {
            --newPlayerRow;
        } else if (direction == 's') {
            ++newPlayerRow;
        } else if (direction == 'a') {
            --newPlayerCol;
        } else if (direction == 'd') {
            ++newPlayerCol;
        }

        if (isValidMove(newPlayerRow, newPlayerCol)) {
            if (isBoxAt(newPlayerRow, newPlayerCol)) {
                int boxIndex = findBoxIndex(newPlayerRow, newPlayerCol);
                int newBoxRow = newPlayerRow + (newPlayerRow - playerRow);
                int newBoxCol = newPlayerCol + (newPlayerCol - playerCol);

                if (isValidMove(newBoxRow, newBoxCol) && !isBoxAt(newBoxRow, newBoxCol)) {
                    moveBox(boxIndex, newBoxRow, newBoxCol);
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

    bool isGameOver() const { return isGameOver; }
    int getPlayerCol() const { return playerCol; }
    int getPlayerRow() const { return playerRow; }

    std::vector<std::shared_ptr<std::pair<int,int>>> getTargets() const {
        return targets;
    }

    int getTargetCount() const { return targetCount; }

    std::vector<std::vector<char>>& getMap() {
        return map;
    }

    std::vector<std::shared_ptr<std::pair<int,int>>> getBoxes() const {
        return boxes;
    }
};