#include <vector>
#include <queue>
#include <set>
#include <string>
#include <utility>

class EightPuzzle {
private:
    std::vector<std::vector<int>> initial_state;
    std::vector<std::vector<int>> goal_state = {{1,2,3},{4,5,6},{7,8,0}};

    static std::string state_to_string(const std::vector<std::vector<int>>& state) {
        std::string s;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                s += ('0' + state[i][j]);
            }
        }
        return s;
    }

    std::pair<int, int> find_blank(const std::vector<std::vector<int>>& state) const {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (state[i][j] == 0) {
                    return {i, j};
                }
            }
        }
        return {-1, -1};
    }

public:
    EightPuzzle(const std::vector<std::vector<int>>& initial_state) : initial_state(initial_state) {}

    std::vector<std::vector<int>> move(const std::vector<std::vector<int>>& state, const std::string& direction) const {
        auto [i, j] = find_blank(state);
        std::vector<std::vector<int>> new_state = state;
        if (direction == "up") {
            std::swap(new_state[i][j], new_state[i-1][j]);
        } else if (direction == "down") {
            std::swap(new_state[i][j], new_state[i+1][j]);
        } else if (direction == "left") {
            std::swap(new_state[i][j], new_state[i][j-1]);
        } else if (direction == "right") {
            std::swap(new_state[i][j], new_state[i][j+1]);
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

    std::vector<std::string> solve() {
        std::queue<std::pair<std::vector<std::vector<int>>, std::vector<std::string>>> open_list;
        std::set<std::string> closed_set;
        open_list.push({initial_state, {}});
        closed_set.insert(state_to_string(initial_state));

        while (!open_list.empty()) {
            auto [current_state, path] = open_list.front();
            open_list.pop();

            if (current_state == goal_state) {
                return path;
            }

            for (const auto& move_dir : get_possible_moves(current_state)) {
                auto new_state = move(current_state, move_dir);
                std::string new_state_str = state_to_string(new_state);
                if (closed_set.find(new_state_str) == closed_set.end()) {
                    closed_set.insert(new_state_str);
                    open_list.push({new_state, path + {move_dir}});
                }
            }
        }
        return {};
    }
};