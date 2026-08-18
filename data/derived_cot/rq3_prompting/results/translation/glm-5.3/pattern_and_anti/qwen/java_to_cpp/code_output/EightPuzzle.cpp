#include <array>
#include <optional>
#include <queue>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace org::example {

class EightPuzzle {
public:
    using State = std::array<std::array<int, 3>, 3>;

    explicit EightPuzzle(const State& initialState)
        : initialState(deepCopy(initialState)),
          goalState{{{{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}}} {}

    // Returns {i, j} of the blank tile; nullopt if not found.
    std::optional<std::array<int, 2>> findBlank(const State& state) const {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (state[i][j] == 0) {
                    return std::array<int, 2>{i, j};
                }
            }
        }
        return std::nullopt;
    }

    State move(const State& state, const std::string& direction) const {
        auto blank = findBlank(state);
        int i = (*blank)[0], j = (*blank)[1];
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

    std::vector<std::string> getPossibleMoves(const State& state) const {
        std::vector<std::string> moves;
        auto blank = findBlank(state);
        int i = (*blank)[0], j = (*blank)[1];

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");

        return moves;
    }

    // Returns the move path to the goal, or nullopt if unsolvable.
    std::optional<std::vector<std::string>> solve() {
        std::queue<Node> openList;                       // FIFO, like LinkedList.poll()
        std::unordered_set<std::string> closedList;
        openList.push(Node{initialState, {}});

        while (!openList.empty()) {
            Node currentNode = openList.front();
            openList.pop();
            const State& currentState = currentNode.state;
            std::vector<std::string> path = std::move(currentNode.path);
            closedList.insert(stateToString(currentState));

            if (currentState == goalState) {             // like Arrays.deepEquals
                return path;
            }

            for (const std::string& moveName : getPossibleMoves(currentState)) {
                State newState = move(currentState, moveName);
                if (closedList.find(stateToString(newState)) == closedList.end()) {
                    std::vector<std::string> newPath = path;
                    newPath.push_back(moveName);
                    openList.push(Node{std::move(newState), std::move(newPath)});
                }
            }
        }
        return std::nullopt;
    }

private:
    struct Node {
        State state;
        std::vector<std::string> path;
    };

    State initialState;
    State goalState;

    static std::string stateToString(const State& state) {
        std::string s;
        for (const auto& row : state) {
            for (int val : row) {
                s += std::to_string(val);
            }
        }
        return s;
    }

    static State deepCopy(const State& original) {
        return original;  // std::array copies by value
    }
};

} // namespace org::example