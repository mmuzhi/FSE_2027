#include <vector>
#include <string>
#include <queue>
#include <unordered_set>
#include <optional>
#include <utility>

class EightPuzzle {
public:
    EightPuzzle(const std::vector<std::vector<int>>& initialState) {
        this->initialState = deepCopy(initialState);
        this->goalState = {{1, 2, 3}, {4, 5, 6}, {7, 8, 0}};
    }

    std::optional<std::pair<int, int>> findBlank(const std::vector<std::vector<int>>& state) const {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (state.at(i).at(j) == 0) {
                    return std::make_pair(i, j);
                }
            }
        }
        return std::nullopt;
    }

    std::vector<std::vector<int>> move(const std::vector<std::vector<int>>& state, const std::string& direction) const {
        std::pair<int, int> blank = findBlank(state).value();
        int i = blank.first;
        int j = blank.second;
        std::vector<std::vector<int>> newState = deepCopy(state);

        if (direction == "up") {
            if (i > 0) {
                newState[i][j] = newState[i - 1][j];
                newState[i - 1][j] = 0;
            }
        } else if (direction == "down") {
            if (i < 2) {
                newState[i][j] = newState[i + 1][j];
                newState[i + 1][j] = 0;
            }
        } else if (direction == "left") {
            if (j > 0) {
                newState[i][j] = newState[i][j - 1];
                newState[i][j - 1] = 0;
            }
        } else if (direction == "right") {
            if (j < 2) {
                newState[i][j] = newState[i][j + 1];
                newState[i][j + 1] = 0;
            }
        }
        return newState;
    }

    std::vector<std::string> getPossibleMoves(const std::vector<std::vector<int>>& state) const {
        std::vector<std::string> moves;
        std::pair<int, int> blank = findBlank(state).value();
        int i = blank.first;
        int j = blank.second;

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");

        return moves;
    }

    std::optional<std::vector<std::string>> solve() const {
        std::queue<Node> openList;
        std::unordered_set<std::string> closedList;
        openList.push(Node(initialState, std::vector<std::string>()));

        while (!openList.empty()) {
            Node currentNode = openList.front();
            openList.pop();
            std::vector<std::vector<int>> currentState = currentNode.state;
            std::vector<std::string> path = currentNode.path;
            closedList.insert(stateToString(currentState));

            if (currentState == goalState) {
                return path;
            }

            for (const std::string& moveDir : getPossibleMoves(currentState)) {
                std::vector<std::vector<int>> newState = move(currentState, moveDir);
                std::string newStateStr = stateToString(newState);
                if (closedList.find(newStateStr) == closedList.end()) {
                    std::vector<std::string> newPath = path;
                    newPath.push_back(moveDir);
                    openList.push(Node(newState, newPath));
                }
            }
        }
        return std::nullopt;
    }

private:
    std::vector<std::vector<int>> initialState;
    std::vector<std::vector<int>> goalState;

    std::string stateToString(const std::vector<std::vector<int>>& state) const {
        std::string s;
        for (const auto& row : state) {
            for (int val : row) {
                s += std::to_string(val);
            }
        }
        return s;
    }

    std::vector<std::vector<int>> deepCopy(const std::vector<std::vector<int>>& original) const {
        std::vector<std::vector<int>> copy;
        copy.reserve(original.size());
        for (const auto& row : original) {
            copy.push_back(row);
        }
        return copy;
    }

    struct Node {
        std::vector<std::vector<int>> state;
        std::vector<std::string> path;

        Node(const std::vector<std::vector<int>>& s, const std::vector<std::string>& p)
            : state(s), path(p) {}
    };
};