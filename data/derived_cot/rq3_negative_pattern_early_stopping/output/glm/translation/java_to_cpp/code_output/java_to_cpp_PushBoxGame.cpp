#include <vector>

class PushBoxGame {
private:
    std::vector<std::vector<char>> map;
    int playerRow;
    int playerCol;
    std::vector<std::vector<int>> targets;
    std::vector<std::vector<int>> boxes;
    int targetCount;
    bool m_isGameOver;

    void initGame() {
        for (int row = 0; row < static_cast<int>(map.size()); row++) {
            for (int col = 0; col < static_cast<int>(map[row].size()); col++) {
                if (map[row][col] == 'O') {
                    this->playerRow = row;
                    this->playerCol = col;
                } else if (map[row][col] == 'G') {
                    this->targets.push_back({row, col});
                    this->targetCount++;
                } else if (map[row][col] == 'X') {
                    this->boxes.push_back({row, col});
                }
            }
        }
    }

    bool isValidMove(int row, int col) {
        return row >= 0 && row < static_cast<int>(map.size()) &&
               col >= 0 && col < static_cast<int>(map[row].size()) &&
               map[row][col] != '#';
    }

    bool isBoxAt(int row, int col) {
        for (const auto& box : boxes) {
            if (box[0] == row && box[1] == col) {
                return true;
            }
        }
        return false;
    }

    std::vector<int>* getBoxPosition(int row, int col) {
        for (auto& box : boxes) {
            if (box[0] == row && box[1] == col) {
                return &box;
            }
        }
        return nullptr;
    }

    void moveBox(const std::vector<int>& boxPosition, int newRow, int newCol) {
        for (size_t i = 0; i < boxes.size(); i++) {
            if (boxes[i] == boxPosition) {
                boxes[i] = {newRow, newCol};
                break;
            }
        }
    }

public:
    PushBoxGame(const std::vector<std::vector<char>>& map)
        : map(map), playerRow(0), playerCol(0), targetCount(0), m_isGameOver(false) {
        initGame();
    }

    bool checkWin() {
        int boxOnTargetCount = 0;
        for (const auto& box : boxes) {
            for (const auto& target : targets) {
                if (box == target) {
                    boxOnTargetCount++;
                }
            }
        }
        m_isGameOver = (boxOnTargetCount == targetCount);
        return m_isGameOver;
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
                std::vector<int>* boxPosition = getBoxPosition(newPlayerRow, newPlayerCol);
                int newBoxRow = newPlayerRow + (newPlayerRow - playerRow);
                int newBoxCol = newPlayerCol + (newPlayerCol - playerCol);

                if (isValidMove(newBoxRow, newBoxCol) && !isBoxAt(newBoxRow, newBoxCol)) {
                    moveBox(*boxPosition, newBoxRow, newBoxCol);
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
        return m_isGameOver;
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

    std::vector<std::vector<char>>& getMap() {
        return map;
    }

    std::vector<std::vector<int>> getBoxes() const {
        return boxes;
    }
};