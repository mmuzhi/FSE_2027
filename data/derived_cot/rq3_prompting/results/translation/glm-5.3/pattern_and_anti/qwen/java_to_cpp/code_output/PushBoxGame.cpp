#include <vector>
#include <array>

class PushBoxGame {
private:
    std::vector<std::vector<char>> map;
    int playerRow;
    int playerCol;
    std::vector<std::array<int, 2>> targets;
    std::vector<std::array<int, 2>> boxes;
    int targetCount;
    bool isGameOver;

    static bool posEquals(const std::array<int, 2>& a, const std::array<int, 2>& b) {
        return a[0] == b[0] && a[1] == b[1];
    }

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
        return row >= 0 && row < static_cast<int>(map.size())
            && col >= 0 && col < static_cast<int>(map[row].size())
            && map[row][col] != '#';
    }

    bool isBoxAt(int row, int col) {
        for (const auto& box : boxes) {
            if (posEquals(box, {row, col})) {
                return true;
            }
        }
        return false;
    }

    // Note: Java version returns null when not found; this call site is
    // always guarded by isBoxAt, so the fallback is never used.
    std::array<int, 2> getBoxPosition(int row, int col) {
        for (const auto& box : boxes) {
            if (posEquals(box, {row, col})) {
                return box;
            }
        }
        return {0, 0};
    }

    void moveBox(const std::array<int, 2>& boxPosition, int newRow, int newCol) {
        for (size_t i = 0; i < boxes.size(); i++) {
            if (posEquals(boxes[i], boxPosition)) {
                boxes[i] = {newRow, newCol};
                break;
            }
        }
    }

public:
    explicit PushBoxGame(const std::vector<std::vector<char>>& map)
        : map(map), playerRow(0), playerCol(0),
          targets(), boxes(), targetCount(0), isGameOver(false) {
        initGame();
    }

    bool checkWin() {
        int boxOnTargetCount = 0;
        for (const auto& box : boxes) {
            for (const auto& target : targets) {
                if (posEquals(box, target)) {
                    boxOnTargetCount++;
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
                std::array<int, 2> boxPosition = getBoxPosition(newPlayerRow, newPlayerCol);
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
        return isGameOver;
    }

    int getPlayerCol() const {
        return playerCol;
    }

    int getPlayerRow() const {
        return playerRow;
    }

    std::vector<std::array<int, 2>> getTargets() const {
        return targets;
    }

    int getTargetCount() const {
        return targetCount;
    }

    // Java returns a reference to the internal map; mirror that semantics.
    std::vector<std::vector<char>>& getMap() {
        return map;
    }

    std::vector<std::array<int, 2>> getBoxes() const {
        return boxes;
    }
};