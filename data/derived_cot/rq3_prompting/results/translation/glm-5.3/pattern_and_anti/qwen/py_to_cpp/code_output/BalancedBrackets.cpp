#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>

class BalancedBrackets {
public:
    explicit BalancedBrackets(const std::string& expr)
        : stack_(),
          left_brackets_{'(', '{', '['},
          right_brackets_{')', '}', ']'},
          expr_(expr) {}

    void clear_expr() {
        std::string filtered;
        for (char c : expr_) {
            if (is_left(c) || is_right(c)) {
                filtered += c;
            }
        }
        expr_ = filtered;
    }

    bool check_balanced_brackets() {
        clear_expr();
        for (char Brkt : expr_) {
            if (is_left(Brkt)) {
                stack_.push_back(Brkt);
            } else {
                // Python: self.stack.pop() on empty list raises IndexError
                if (stack_.empty()) {
                    throw std::out_of_range("pop from empty list");
                }
                char Current_Brkt = stack_.back();
                stack_.pop_back();
                if (Current_Brkt == '(') {
                    if (Brkt != ')') {
                        return false;
                    }
                }
                if (Current_Brkt == '{') {
                    if (Brkt != '}') {
                        return false;
                    }
                }
                if (Current_Brkt == '[') {
                    if (Brkt != ']') {
                        return false;
                    }
                }
            }
        }
        if (!stack_.empty()) {
            return false;
        }
        return true;
    }

private:
    std::vector<char> stack_;
    std::vector<char> left_brackets_{'(', '{', '['};
    std::vector<char> right_brackets_{')', '}', ']'};
    std::string expr_;

    bool is_left(char c) const {
        return std::find(left_brackets_.begin(), left_brackets_.end(), c) != left_brackets_.end();
    }

    bool is_right(char c) const {
        return std::find(right_brackets_.begin(), right_brackets_.end(), c) != right_brackets_.end();
    }
};