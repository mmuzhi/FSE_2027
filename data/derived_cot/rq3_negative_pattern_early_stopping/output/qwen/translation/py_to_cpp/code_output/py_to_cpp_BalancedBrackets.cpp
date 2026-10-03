#include <vector>
#include <string>
#include <stdexcept>

class BalancedBrackets {
private:
    std::vector<char> stack;
    const char left_brackets[3] = {'(', '{', '['};
    const char right_brackets[3] = {')', '}', ']'};
    std::string expr;

public:
    BalancedBrackets(const std::string& expr) : expr(expr) {}

    void clear_expr() {
        std::string new_expr;
        for (char c : expr) {
            if (c == left_brackets[0] || c == left_brackets[1] || c == left_brackets[2] ||
                c == right_brackets[0] || c == right_brackets[1] || c == right_brackets[2]) {
                new_expr += c;
            }
        }
        expr = new_expr;
    }

    bool check_balanced_brackets() {
        clear_expr();
        for (char Brkt : expr) {
            if (Brkt == left_brackets[0] || Brkt == left_brackets[1] || Brkt == left_brackets[2]) {
                stack.push_back(Brkt);
            } else {
                if (stack.empty()) {
                    throw std::runtime_error("Stack underflow");
                }
                char top = stack.back();
                stack.pop_back();
                if (top == '(' && Brkt != ')') return false;
                if (top == '{' && Brkt != '}') return false;
                if (top == '[' && Brkt != ']') return false;
            }
        }
        return stack.empty();
    }
};