#include <stdexcept>
#include <string>
#include <vector>

class BalancedBrackets {
public:
    std::vector<char> stack;
    std::vector<std::string> left_brackets;
    std::vector<std::string> right_brackets;
    std::string expr;

    BalancedBrackets(const std::string& expr)
        : stack(),
          left_brackets({"(", "{", "["}),
          right_brackets({")", "}", "]"}),
          expr(expr) {}

    void clear_expr() {
        std::string filtered;
        for (char c : expr) {
            if (is_left_bracket(c) || is_right_bracket(c)) {
                filtered += c;
            }
        }
        expr = filtered;
    }

    bool check_balanced_brackets() {
        clear_expr();
        for (char Brkt : expr) {
            if (is_left_bracket(Brkt)) {
                stack.push_back(Brkt);
            } else {
                if (stack.empty()) {
                    // Python list.pop() on an empty list raises IndexError
                    throw std::out_of_range("IndexError: pop from empty list");
                }
                char Current_Brkt = stack.back();
                stack.pop_back();
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
        if (!stack.empty()) {
            return false;
        }
        return true;
    }

private:
    bool is_left_bracket(char c) const {
        for (const std::string& b : left_brackets) {
            if (b.size() == 1 && b[0] == c) return true;
        }
        return false;
    }

    bool is_right_bracket(char c) const {
        for (const std::string& b : right_brackets) {
            if (b.size() == 1 && b[0] == c) return true;
        }
        return false;
    }
};