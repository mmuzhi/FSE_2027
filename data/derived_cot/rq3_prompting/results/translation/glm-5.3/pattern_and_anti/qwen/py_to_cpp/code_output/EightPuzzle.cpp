#include <vector>
#include <string>
#include <deque>
#include <utility>
#include <optional>
#include <stdexcept>
#include <algorithm>

class EightPuzzle {
public:
    using State = std::vector<std::vector<int>>;
    using Position = std::pair<int, int>;

    State initial_state;
    State goal_state = {{1, 2, 3}, {4, 5, 6}, {7, 8, 0}};

    explicit EightPuzzle(State initial_state_)
        : initial_state(std::move(initial_state_)) {}

    // Returns the coordinate of the blank block (0 element),
    // or std::nullopt if no blank exists (mirrors Python returning None).
    std::optional<Position> find_blank(const State& state) const {
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
        if (!blank.has_value()) {
            // Mirrors Python's TypeError when unpacking a None return value.
            throw std::runtime_error("cannot unpack non-iterable NoneType object");
        }
        int i = blank->first;
        int j = blank->second;

        State new_state = state;

        int ni = i, nj = j;
        if (direction == "up") {
            ni = i - 1;
        } else if (direction == "down") {
            ni = i + 1;
        } else if (direction == "left") {
            nj = j - 1;
        } else if (direction == "right") {
            nj = j + 1;
        }

        // Python negative indices wrap around (e.g., -1 -> last element).
        if (ni < 0) ni += 3;
        if (nj < 0) nj += 3;
        // Python positive out-of-range indices raise IndexError.
        if (ni >= 3 || nj >= 3) {
            throw std::out_of_range("list index out of range");
        }

        std::swap(new_state[i][j], new_state[ni][nj]);
        return new_state;
    }

    std::vector<std::string> get_possible_moves(const State& state) const {
        std::vector<std::string> moves;
        auto blank = find_blank(state);
        if (!blank.has_value()) {
            throw std::runtime_error("cannot unpack non-iterable NoneType object");
        }
        int i = blank->first;
        int j = blank->second;

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");

        return moves;
    }

    // Returns the solution path, or std::nullopt if unsolvable (mirrors Python's None).
    std::optional<std::vector<std::string>> solve() {
        std::deque<std::pair<State, std::vector<std::string>>> open_list;
        std::vector<State> closed_list;

        open_list.emplace_back(initial_state, std::vector<std::string>{});

        while (!open_list.empty()) {
            auto [current_state, path] = std::move(open_list.front());
            open_list.pop_front();
            closed_list.push_back(current_state);

            if (current_state == goal_state) {
                return path;
            }

            for (const auto& mv : get_possible_moves(current_state)) {
                State new_state = this->move(current_state, mv);
                if (std::find(closed_list.begin(), closed_list.end(), new_state) == closed_list.end()) {
                    std::vector<std::string> new_path = path;
                    new_path.push_back(mv);
                    open_list.emplace_back(std::move(new_state), std::move(new_path));
                }
            }
        }

        return std::nullopt;
    }
};