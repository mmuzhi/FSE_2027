#include <vector>
#include <string>
#include <queue>
#include <unordered_set>
#include <optional>
#include <sstream>
#include <utility>

class EightPuzzle {
private:
    std::vector<std::vector<int>> initialState;
    std::vector<std::vector<int>> goalState;

    struct Node {
        std::vector<std::vector<int>> state;
        std::vector<std::string> path;
        Node(const std::vector<std::vector<int>>& s, const std::vector<std::string>& p)
            : state(s), path(p) {}
    };

    // Find the position of the blank (0) in the state
    std::pair<int, int> findBlank(const std::vector<std::vector<int>>& state) const {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (state[i][j] == 0) {
                    return {i, j};
                }
            }
        }
        // Should never happen for a valid puzzle
        return {-1, -1};
    }

    // Deep copy a 2D vector
    std::vector<std::vector<int>> deepCopy(const std::vector<std::vector<int>>& original) const {
        std::vector<std::vector<int>> copy;
        copy.reserve(original.size());
        for (const auto& row : original) {
            copy.push_back(row); // vector copy is deep
        }
        return copy;
    }

    // Convert state to a string for hashing / comparison
    std::string stateToString(const std::vector<std::vector<int>>& state) const {
        std::ostringstream oss;
        for (const auto& row : state) {
            for (int val : row) {
                oss << val;
            }
        }
        return oss.str();
    }

public:
    EightPuzzle(const std::vector<std::vector<int>>& initialState)
        : initialState(deepCopy(initialState)),
          goalState({{1,2,3}, {4,5,6}, {7,8,0}}) {}

    // Apply a move to a state, returning the new state (or the same if move is invalid)
    std::vector<std::vector<int>> move(const std::vector<std::vector<int>>& state,
                                        const std::string& direction) const {
        auto [i, j] = findBlank(state);
        std::vector<std::vector<int>> newState = deepCopy(state);

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

    // Return list of possible moves from a given state
    std::vector<std::string> getPossibleMoves(const std::vector<std::vector<int>>& state) const {
        auto [i, j] = findBlank(state);
        std::vector<std::string> moves;
        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");
        return moves;
    }

    // BFS solver: returns path if solvable, std::nullopt otherwise
    std::optional<std::vector<std::string>> solve() {
        std::queue<Node> openList;
        std::unordered_set<std::string> closedList;

        openList.push(Node(initialState, {}));

        while (!openList.empty()) {
            Node currentNode = openList.front();
            openList.pop();
            const auto& currentState = currentNode.state;
            const auto& path = currentNode.path;

            closedList.insert(stateToString(currentState));

            if (currentState == goalState) {
                return path;
            }

            for (const auto& moveStr : getPossibleMoves(currentState)) {
                std::vector<std::vector<int>> newState = move(currentState, moveStr);
                std::string stateKey = stateToString(newState);
                if (closedList.find(stateKey) == closedList.end()) {
                    std::vector<std::string> newPath = path;
                    newPath.push_back(moveStr);
                    openList.push(Node(newState, newPath));
                }
            }
        }
        return std::nullopt;
    }
};