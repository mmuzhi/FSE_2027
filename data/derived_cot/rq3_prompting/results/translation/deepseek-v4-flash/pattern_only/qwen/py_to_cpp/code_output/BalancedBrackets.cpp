#include <string>
#include <stack>
#include <stdexcept>

class BalancedBrackets {
private:
    std::stack<char> stack;
    std::string left_brackets = "({[";
    std::string right_brackets = ")}]";
    std::string expr;

public:
    BalancedBrackets(const std::string& expr) : expr(expr) {}

    void clear_expr() {
        std::string result;
        for (char c : expr) {
            if (left_brackets.find(c) != std::string::npos ||
                right_brackets.find(c) != std::string::npos) {
                result += c;
            }
        }
        expr = result;
    }

    bool check_balanced_brackets() {
        clear_expr();
        for (char Brkt : expr) {
            if (left_brackets.find(Brkt) != std::string::npos) {
                stack.push(Brkt);
            } else {
                if (stack.empty()) {
                    throw std::out_of_range("pop from empty stack");
                }
                char Current_Brkt = stack.top();
                stack.pop();
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
        if (!stack.empty()) return false;
        return true;
    }
};