#include <vector>
#include <utility>
#include <algorithm>

class PushBoxGame {
private:
    std::vector<std::vector<char>> map;
    int playerRow;
    int playerCol;
    std::vector<std::pair<int, int>> targets;
    std::vector<std::pair<int, int>> boxes;
    int targetCount;
    bool isGameOver;

    void initGame() {
        for (int row = 0; row < static_cast<int>(map.size()); ++row) {
            for (int col = 0; col < static_cast<int>(map[row].size()); ++col) {
                char c = map[row][col];
                if (c == 'O') {
                    playerRow = row;
                    playerCol = col;
                } else if (c == 'G') {
                    targets.emplace_back(row, col);
                    ++targetCount;
                } else if (c == 'X') {
                    boxes.emplace_back(row, col);
                }
            }
        }
    }

    bool isValidMove(int row, int col) const {
        if (row < 0 || row >= static_cast<int>(map.size())) return false;
        if (col < 0 || col >= static_cast<int>(map[row].size())) return false;
        return map[row][col] != '#';
    }

    bool isBoxAt(int row, int col) const {
        for (const auto& box : boxes) {
            if (box.first == row && box.second == col) {
                return true;
            }
        }
        return false;
    }

    // Returns index of box at (row, col). Assumes such a box exists.
    int getBoxIndex(int row, int col) const {
        for (std::size_t i = 0; i < boxes.size(); ++i) {
            if (boxes[i].first == row && boxes[i].second == col) {
                return static_cast<int>(i);
            }
        }
        return -1; // Should never happen because isBoxAt was true.
    }

public:
    PushBoxGame(const std::vector<std::vector<char>>& map)
        : map(map),
          playerRow(0),
          playerCol(0),
          targetCount(0),
          isGameOver(false)
    {
        initGame();
    }

    bool checkWin() {
        int boxOnTargetCount = 0;
        for (const auto& box : boxes) {
            for (const auto& target : targets) {
                if (box == target) {
                    ++boxOnTargetCount;
                    break;
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
        } else {
            // unrecognized direction, no move
            return checkWin();
        }

        if (isValidMove(newPlayerRow, newPlayerCol)) {
            if (isBoxAt(newPlayerRow, newPlayerCol)) {
                int boxIndex = getBoxIndex(newPlayerRow, newPlayerCol);
                int newBoxRow = newPlayerRow + (newPlayerRow - playerRow);
                int newBoxCol = newPlayerCol + (newPlayerCol - playerCol);

                if (isValidMove(newBoxRow, newBoxCol) && !isBoxAt(newBoxRow, newBoxCol)) {
                    // Move the box
                    boxes[boxIndex] = {newBoxRow, newBoxCol};
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

    std::vector<std::pair<int, int>> getTargets() const {
        return targets; // copy
    }

    int getTargetCount() const {
        return targetCount;
    }

    const std::vector<std::vector<char>>& getMap() const {
        return map;
    }

    std::vector<std::pair<int, int>> getBoxes() const {
        return boxes; // copy
    }
};