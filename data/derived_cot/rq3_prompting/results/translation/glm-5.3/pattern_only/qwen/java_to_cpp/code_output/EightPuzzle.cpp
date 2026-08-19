#pragma once

#include <array>
#include <optional>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace org {
namespace example {

class EightPuzzle {
public:
    using State = std::array<std::array<int, 3>, 3>;

    explicit EightPuzzle(const State& initialState)
        : initialState_(deepCopy(initialState)),
          goalState_{{{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}} {}

    // Java returns null when no blank exists.
    std::optional<std::pair<int, int>> findBlank(const State& state) const {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (state[i][j] == 0) {
                    return std::make_pair(i, j);
                }
            }
        }
        return std::nullopt;
    }

    State move(const State& state, const std::string& direction) const {
        std::optional<std::pair<int, int>> blank = findBlank(state);
        // Java would throw NullPointerException on null dereference.
        if (!blank.has_value()) {
            throw std::runtime_error("NullPointerException: blank not found");
        }
        int i = blank->first, j = blank->second;
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
        std::optional<std::pair<int, int>> blank = findBlank(state);
        // Java would throw NullPointerException on null dereference.
        if (!blank.has_value()) {
            throw std::runtime_error("NullPointerException: blank not found");
        }
        int i = blank->first, j = blank->second;

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");

        return moves;
    }

    // Java returns null when no solution exists.
    std::optional<std::vector<std::string>> solve() {
        std::queue<Node> openList;
        std::unordered_set<std::string> closedList;
        openList.push(Node(initialState_, std::vector<std::string>()));

        while (!openList.empty()) {
            Node currentNode = std::move(openList.front());
            openList.pop();
            State currentState = currentNode.state;
            std::vector<std::string> path = std::move(currentNode.path);
            closedList.insert(stateToString(currentState));

            if (currentState == goalState) {
                return path;
            }

            for (const std::string& moveName : getPossibleMoves(currentState)) {
                State newState = move(currentState, moveName);
                if (closedList.find(stateToString(newState)) == closedList.end()) {
                    std::vector<std::string> newPath = path;
                    newPath.push_back(moveName);
                    openList.push(Node(newState, std::move(newPath)));
                }
            }
        }
        return std::nullopt;
    }

private:
    struct Node {
        State state;
        std::vector<std::string> path;

        Node(const State& state, std::vector<std::string> path)
            : state(state), path(std::move(path)) {}
    };

    State initialState_;
    State goalState_;

    static std::string stateToString(const State& state) {
        std::string sb;
        for (const auto& row : state) {
            for (int val : row) {
                sb += std::to_string(val);
            }
        }
        return sb;
    }

    static State deepCopy(const State& original) {
        // std::array is a value type; copying it is equivalent to a deep copy.
        return original;
    }
};

} // namespace example
} // namespace org