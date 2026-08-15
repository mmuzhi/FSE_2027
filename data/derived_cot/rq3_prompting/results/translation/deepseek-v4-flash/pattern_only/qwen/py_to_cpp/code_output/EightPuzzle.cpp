#include <array>
#include <vector>
#include <string>
#include <queue>
#include <optional>
#include <algorithm>
#include <stdexcept>
#include <utility>

class EightPuzzle {
public:
    using State = std::array<std::array<int, 3>, 3>;

    State initial_state;
    State goal_state;

    EightPuzzle(State initial_state)
        : initial_state(initial_state),
          goal_state({{{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}}) {}

    std::optional<std::pair<int, int>> find_blank(const State& state) const {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (state[i][j] == 0) {
                    return std::make_pair(i, j);
                }
            }
        }
        return std::nullopt;
    }

    State move(const State& state, const std::string& direction) const {
        auto blank = find_blank(state);
        if (!blank) {
            throw std::runtime_error("No blank tile found");
        }

        int i = blank->first;
        int j = blank->second;
        State new_state = state;

        if (direction == "up") {
            int ni = (i - 1 + 3) % 3;
            std::swap(new_state[i][j], new_state[ni][j]);
        } else if (direction == "down") {
            if (i + 1 >= 3) {
                throw std::out_of_range("list index out of range");
            }
            std::swap(new_state[i][j], new_state[i + 1][j]);
        } else if (direction == "left") {
            int nj = (j - 1 + 3) % 3;
            std::swap(new_state[i][j], new_state[i][nj]);
        } else if (direction == "right") {
            if (j + 1 >= 3) {
                throw std::out_of_range("list index out of range");
            }
            std::swap(new_state[i][j], new_state[i][j + 1]);
        }

        return new_state;
    }

    std::vector<std::string> get_possible_moves(const State& state) const {
        std::vector<std::string> moves;
        auto blank = find_blank(state);
        if (!blank) {
            throw std::runtime_error("No blank tile found");
        }

        int i = blank->first;
        int j = blank->second;

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");

        return moves;
    }

    std::optional<std::vector<std::string>> solve() const {
        std::queue<std::pair<State, std::vector<std::string>>> open_list;
        open_list.push({initial_state, {}});

        std::vector<State> closed_list;

        while (!open_list.empty()) {
            auto [current_state, path] = open_list.front();
            open_list.pop();

            closed_list.push_back(current_state);

            if (current_state == goal_state) {
                return path;
            }

            for (const auto& move_dir : get_possible_moves(current_state)) {
                State new_state = move(current_state, move_dir);

                if (std::find(closed_list.begin(), closed_list.end(), new_state) == closed_list.end()) {
                    auto new_path = path;
                    new_path.push_back(move_dir);
                    open_list.push({new_state, new_path});
                }
            }
        }

        return std::nullopt;
    }
};