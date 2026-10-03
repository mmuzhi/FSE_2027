#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>

class BalancedBrackets {
private:
    std::vector<char> stack;
    std::vector<char> left_brackets;
    std::vector<char> right_brackets;
    std::string expr;

public:
    BalancedBrackets(const std::string& expr)
        : stack(),
          left_brackets{'(', '{', '['},
          right_brackets{')', '}', ']'},
          expr(expr) {}

    void clear_expr() {
        std::string filtered;
        for (char c : expr) {
            if (std::find(left_brackets.begin(), left_brackets.end(), c) != left_brackets.end() ||
                std::find(right_brackets.begin(), right_brackets.end(), c) != right_brackets.end()) {
                filtered += c;
            }
        }
        expr = filtered;
    }

    bool check_balanced_brackets() {
        clear_expr();
        for (char Brkt : expr) {
            if (std::find(left_brackets.begin(), left_brackets.end(), Brkt) != left_brackets.end()) {
                stack.push_back(Brkt);
            } else {
                if (stack.empty()) {
                    throw std::runtime_error("IndexError: pop from empty list");
                }
                char Current_Brkt = stack.back();
                stack.pop_back();
                if (Current_Brkt == '(') {
                    if (Brkt != ')') return false;
                }
                if (Current_Brkt == '{') {
                    if (Brkt != '}') return false;
                }
                if (Current_Brkt == '[') {
                    if (Brkt != ']') return false;
                }
            }
        }
        if (!stack.empty()) {
            return false;
        }
        return true;
    }
};