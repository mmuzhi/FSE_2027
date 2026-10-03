#include <vector>
#include <string>
#include <utility>
#include <algorithm>
#include <queue>
#include <optional>

class EightPuzzle {
private:
    std::vector<std::vector<int>> initial_state;
    std::vector<std::vector<int>> goal_state;

public:
    EightPuzzle(std::vector<std::vector<int>> initial_state)
        : initial_state(std::move(initial_state)), 
          goal_state({{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}) {}

    std::pair<int, int> find_blank(const std::vector<std::vector<int>>& state) const {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (state[i][j] == 0) {
                    return {i, j};
                }
            }
        }
        return {-1, -1}; // Fallback, should not happen with valid puzzle states
    }

    std::vector<std::vector<int>> move(const std::vector<std::vector<int>>& state, const std::string& direction) const {
        auto [i, j] = find_blank(state);
        std::vector<std::vector<int>> new_state = state;

        if (direction == "up") {
            std::swap(new_state[i][j], new_state[i - 1][j]);
        } else if (direction == "down") {
            std::swap(new_state[i][j], new_state[i + 1][j]);
        } else if (direction == "left") {
            std::swap(new_state[i][j], new_state[i][j - 1]);
        } else if (direction == "right") {
            std::swap(new_state[i][j], new_state[i][j + 1]);
        }

        return new_state;
    }

    std::vector<std::string> get_possible_moves(const std::vector<std::vector<int>>& state) const {
        std::vector<std::string> moves;
        auto [i, j] = find_blank(state);

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");

        return moves;
    }

    std::optional<std::vector<std::string>> solve() {
        // Queue stores pairs of {current_state, path_to_state}
        std::queue<std::pair<std::vector<std::vector<int>>, std::vector<std::string>>> open_list;
        std::vector<std::vector<std::vector<int>>> closed_list;

        open_list.emplace(initial_state, std::vector<std::string>{});

        while (!open_list.empty()) {
            auto [current_state, path] = open_list.front();
            open_list.pop();

            closed_list.push_back(current_state);

            if (current_state == goal_state) {
                return path;
            }

            for (const auto& move_dir : get_possible_moves(current_state)) {
                auto new_state = move(current_state, move_dir);
                
                // Check if new_state is not in closed_list
                if (std::find(closed_list.begin(), closed_list.end(), new_state) == closed_list.end()) {
                    std::vector<std::string> new_path = path;
                    new_path.push_back(move_dir);
                    open_list.emplace(std::move(new_state), std::move(new_path));
                }
            }
        }

        return std::nullopt; // Equivalent to Python's None
    }
};