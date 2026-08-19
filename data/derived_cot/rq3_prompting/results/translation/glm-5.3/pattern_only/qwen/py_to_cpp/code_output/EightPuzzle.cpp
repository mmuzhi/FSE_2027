#include <array>
#include <deque>
#include <optional>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class EightPuzzle {
public:
    // Equivalent of Python's 3x3 list-of-lists state (value semantics: ==, <, copy).
    using State = std::array<std::array<int, 3>, 3>;

    State initial_state;
    State goal_state;

    explicit EightPuzzle(const State& initial_state)
        : initial_state(initial_state),
          goal_state{{{1, 2, 3}, {4, 5, 6}, {7, 8, 0}}} {}

    // Returns (row, col) of the 0 tile; std::nullopt mirrors Python's implicit None.
    std::optional<std::pair<int, int>> find_blank(const State& state) const {
        for (int i = 0; i < 3; ++i) {
            for (int j = 0; j < 3; ++j) {
                if (state[i][j] == 0) return std::make_pair(i, j);
            }
        }
        return std::nullopt;
    }

    State move(const State& state, const std::string& direction) const {
        auto [i, j] = blank_or_throw(state);
        State new_state = state;  // deep copy, like [row[:] for row in state]

        if (direction == "up") {
            int r = (i - 1 < 0) ? i - 1 + 3 : i - 1;  // Python negative index wraps to last row
            std::swap(new_state[i][j], new_state[r][j]);
        } else if (direction == "down") {
            int r = i + 1;
            if (r >= 3) throw std::out_of_range("list index out of range");  // IndexError
            std::swap(new_state[i][j], new_state[r][j]);
        } else if (direction == "left") {
            int c = (j - 1 < 0) ? j - 1 + 3 : j - 1;  // Python negative index wraps to last column
            std::swap(new_state[i][j], new_state[i][c]);
        } else if (direction == "right") {
            int c = j + 1;
            if (c >= 3) throw std::out_of_range("list index out of range");  // IndexError
            std::swap(new_state[i][j], new_state[i][c]);
        }
        // Unknown direction: return an unchanged copy, exactly like the Python branch fallthrough.
        return new_state;
    }

    std::vector<std::string> get_possible_moves(const State& state) const {
        std::vector<std::string> moves;
        auto [i, j] = blank_or_throw(state);

        if (i > 0) moves.push_back("up");
        if (i < 2) moves.push_back("down");
        if (j > 0) moves.push_back("left");
        if (j < 2) moves.push_back("right");
        return moves;
    }

    // std::nullopt mirrors Python's None for an unsolvable puzzle.
    std::optional<std::vector<std::string>> solve() const {
        // FIFO queue, matching open_list.pop(0) semantics.
        std::deque<std::pair<State, std::vector<std::string>>> open_list;
        std::set<State> closed_list;

        open_list.emplace_back(initial_state, std::vector<std::string>{});

        while (!open_list.empty()) {
            auto [current_state, path] = std::move(open_list.front());
            open_list.pop_front();
            closed_list.insert(current_state);

            if (current_state == goal_state) {
                return path;
            }

            for (const std::string& mv : get_possible_moves(current_state)) {
                State new_state = move(current_state, mv);
                if (closed_list.count(new_state) == 0) {
                    std::vector<std::string> new_path = path;
                    new_path.push_back(mv);  // path + [move]
                    open_list.emplace_back(std::move(new_state), std::move(new_path));
                }
            }
        }
        return std::nullopt;
    }

private:
    std::pair<int, int> blank_or_throw(const State& state) const {
        auto blank = find_blank(state);
        if (!blank.has_value()) {
            // Python raises TypeError when unpacking a None return value.
            throw std::runtime_error("cannot unpack non-iterable NoneType");
        }
        return *blank;
    }
};