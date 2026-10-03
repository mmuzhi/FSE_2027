#include <vector>
#include <utility> // for std::pair

class PushBoxGame {
private:
    std::vector<std::vector<char>> map;
    int playerRow;
    int playerCol;
    std::vector<std::pair<int, int>> targets;
    std::vector<std::pair<int, int>> boxes;
    int targetCount;
    bool isGameOver;

    void initGame();

    bool isValidMove(int row, int col) const;
    bool isBoxAt(int row, int col) const;
    std::pair<int, int> getBoxPosition(int row, int col) const;
    void moveBox(const std::pair<int, int>& boxPosition, int newRow, int newCol);

public:
    PushBoxGame(const std::vector<std::vector<char>>& map);
    bool checkWin();
    bool move(char direction);
    bool isGameOver() const { return isGameOver; }
    int getPlayerCol() const { return playerCol; }
    int getPlayerRow() const { return playerRow; }
    const std::vector<std::pair<int, int>>& getTargets() const { return targets; }
    int getTargetCount() const { return targetCount; }
    const std::vector<std::vector<char>>& getMap() const { return map; }
    const std::vector<std::pair<int, int>>& getBoxes() const { return boxes; }
};

PushBoxGame::PushBoxGame(const std::vector<std::vector<char>>& mapData)
    : map(mapData), playerRow(0), playerCol(0), targetCount(0), isGameOver(false) {
    initGame();
}

void PushBoxGame::initGame() {
    playerRow = 0;
    playerCol = 0;
    targets.clear();
    boxes.clear();
    targetCount = 0;
    isGameOver = false;

    for (int row = 0; row < map.size(); ++row) {
        for (int col = 0; col < map[row].size(); ++col) {
            if (map[row][col] == 'O') {
                playerRow = row;
                playerCol = col;
            } else if (map[row][col] == 'G') {
                targets.emplace_back(row, col);
                ++targetCount;
            } else if (map[row][col] == 'X') {
                boxes.emplace_back(row, col);
            }
        }
    }
}

bool PushBoxGame::checkWin() {
    int boxOnTargetCount = 0;
    for (const auto& box : boxes) {
        for (const auto& target : targets) {
            if (box == target) {
                ++boxOnTargetCount;
            }
        }
    }
    isGameOver = (boxOnTargetCount == targetCount);
    return isGameOver;
}

bool PushBoxGame::move(char direction) {
    int newPlayerRow = playerRow;
    int newPlayerCol = playerCol;

    switch (direction) {
        case 'w': newPlayerRow--; break;
        case 's': newPlayerRow++; break;
        case 'a': newPlayerCol--; break;
        case 'd': newPlayerCol++; break;
        default: return checkWin();
    }

    if (!isValidMove(newPlayerRow, newPlayerCol)) {
        return checkWin();
    }

    if (isBoxAt(newPlayerRow, newPlayerCol)) {
        auto boxPosition = getBoxPosition(newPlayerRow, newPlayerCol);
        int newBoxRow = newPlayerRow + (newPlayerRow - playerRow);
        int newBoxCol = newPlayerCol + (newPlayerCol - playerCol);

        if (isValidMove(newBoxRow, newBoxCol) && !isBoxAt(newBoxRow, newBoxCol)) {
            moveBox(boxPosition, newBoxRow, newBoxCol);
        } else {
            return checkWin();
        }
    }

    playerRow = newPlayerRow;
    playerCol = newPlayerCol;
    return checkWin();
}

bool PushBoxGame::isValidMove(int row, int col) const {
    return (row >= 0 && row < map.size() && col >= 0 && col < map[row].size() && map[row][col] != '#');
}

bool PushBoxGame::isBoxAt(int row, int col) const {
    for (const auto& box : boxes) {
        if (box == std::make_pair(row, col)) {
            return true;
        }
    }
    return false;
}

std::pair<int, int> PushBoxGame::getBoxPosition(int row, int col) const {
    for (const auto& box : boxes) {
        if (box == std::make_pair(row, col)) {
            return box;
        }
    }
    return std::make_pair(-1, -1); // Should not happen if isBoxAt returns true
}

void PushBoxGame::moveBox(const std::pair<int, int>& boxPosition, int newRow, int newCol) {
    for (auto& box : boxes) {
        if (box == boxPosition) {
            box = std::make_pair(newRow, newCol);
            break;
        }
    }
}