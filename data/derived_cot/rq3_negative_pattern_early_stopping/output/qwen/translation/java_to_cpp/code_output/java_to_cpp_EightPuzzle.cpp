#include <vector>
#include <string>
#include <queue>
#include <unordered_set>
#include <optional>
#include <algorithm>

class EightPuzzle {
private:
    std::vector<std::vector<int>> initialState;
    std::vector<std::vector<int>> goalState;

    // Helper function to find the blank (0) in the state
    std::optional<std::pair<int, int>> findBlank(const std::vector<std::vector<int>>& state) const {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (state[i][j] == 0) {
                    return {{i, j}};
                }
            }
        }
        return std::nullopt;
    }

    // Helper function to convert state to a string for hashing
    std::string stateToString(const std::vector<std::vector<int>>& state) const {
        std::string s;
        for (const auto& row : state) {
            for (int num : row) {
                s += std::to_string(num);
            }
        }
        return s;
    }

    // Helper function to perform a move on the state
    std::vector<std::vector<int>> move(const std::vector<std::vector<int>>& state, const std::string& direction) const {
        auto blank = findBlank(state);
        if (!blank) {
            return state; // Return original state if no blank found
        }
        int i = blank->first, j = blank->second;
        auto newState = state;

        if (direction == "up" && i > 0) {
            std::swap(newState[i][j], newState[i-1][j]);
        } else if (direction == "down" && i < 2) {
            std::swap(newState[i][j], newState[i+1][j]);
        } else if (direction == "left" && j > 0) {
            std::swap(newState[i][j], newState[i][j-1]);
        } else if (direction == "right" && j < 2) {
            std::swap(newState[i][j], newState[i][j+1]);
        }
        return newState;
    }

    // Helper function to get all possible moves from the current state
    std::vector<std::string> getPossibleMoves(const std::vector<std::vector<int>>& state) const {
        auto blank = findBlank(state);
        if (!blank) {
            return {};
        }
        int i = blank->first, j = blank->second;
        std::vector<std::string> moves;
        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");
        return moves;
    }

public:
    EightPuzzle(const std::vector<std::vector<int>>& initialState) 
        : initialState(initialState), 
          goalState({{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}) {}

    // BFS to solve the puzzle
    std::vector<std::string> solve() const {
        struct Node {
            std::vector<std::vector<int>> state;
            std::vector<std::string> path;
        };

        std::queue<Node> openList;
        std::unordered_set<std::string> closedList;

        Node start;
        start.state = initialState;
        start.path = {};
        openList.push(start);

        while (!openList.empty()) {
            Node currentNode = openList.front();
            openList.pop();

            std::string stateStr = stateToString(currentNode.state);
            if (closedList.find(stateStr) != closedList.end()) {
                continue;
            }
            closedList.insert(stateStr);

            if (stateToString(currentNode.state) == stateToString(goalState)) {
                return currentNode.path;
            }

            for (const auto& move : getPossibleMoves(currentNode.state)) {
                Node newNode;
                newNode.state = move(currentNode.state, move);
                newNode.path = currentNode.path;
                newNode.path.push_back(move);
                openList.push(newNode);
            }
        }

        return {};
    }
};