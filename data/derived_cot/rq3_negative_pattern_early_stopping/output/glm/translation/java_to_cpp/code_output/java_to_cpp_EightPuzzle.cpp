#include <vector>
#include <string>
#include <queue>
#include <unordered_set>
#include <optional>
#include <utility>

class EightPuzzle {
private:
    using State = std::vector<std::vector<int>>;
    using Path = std::vector<std::string>;

    State initialState;
    State goalState;

    struct Node {
        State state;
        Path path;
    };

    static State deepCopy(const State& original) {
        State copy;
        copy.reserve(original.size());
        for (const auto& row : original) {
            copy.push_back(row);
        }
        return copy;
    }

    static std::string stateToString(const State& state) {
        std::string s;
        for (const auto& row : state) {
            for (int val : row) {
                s += std::to_string(val);
            }
        }
        return s;
    }

public:
    EightPuzzle(const std::vector<std::vector<int>>& initialState) : initialState(deepCopy(initialState)), goalState({{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}) {}

    std::vector<int> findBlank(const std::vector<std::vector<int>>& state) {
        for (size_t i = 0; i < state.size(); i++) {
            for (size_t j = 0; j < state[i].size(); j++) {
                if (state[i][j] == 0) {
                    return {static_cast<int>(i), static_cast<int>(j)};
                }
            }
        }
        return {};
    }

    std::vector<std::vector<int>> move(const std::vector<std::vector<int>>& state, const std::string& direction) {
        std::vector<int> blank = findBlank(state);
        int i = blank[0], j = blank[1];
        State newState = deepCopy(state);

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

    std::vector<std::string> getPossibleMoves(const std::vector<std::vector<int>>& state) {
        Path moves;
        std::vector<int> blank = findBlank(state);
        int i = blank[0], j = blank[1];

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");

        return moves;
    }

    std::optional<std::vector<std::string>> solve() {
        std::queue<Node> openList;
        std::unordered_set<std::string> closedList;
        openList.push({initialState, {}});

        while (!openList.empty()) {
            Node currentNode = std::move(openList.front());
            openList.pop();
            State currentState = std::move(currentNode.state);
            Path path = std::move(currentNode.path);
            closedList.insert(stateToString(currentState));

            if (currentState == goalState) {
                return path;
            }

            for (const std::string& moveDir : getPossibleMoves(currentState)) {
                State newState = move(currentState, moveDir);
                if (closedList.find(stateToString(newState)) == closedList.end()) {
                    Path newPath = path;
                    newPath.push_back(moveDir);
                    openList.push({std::move(newState), std::move(newPath)});
                }
            }
        }
        return std::nullopt;
    }
};