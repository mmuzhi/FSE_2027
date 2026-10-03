#include <string>
#include <vector>

class BalancedBrackets {
private:
    std::vector<char> stack;
    std::string left_brackets = "({[";
    std::string right_brackets = ")}]";
    std::string expr;

public:
    // Constructor: initializes with the given expression
    BalancedBrackets(const std::string& expr)
        : expr(expr) {}

    // Removes all characters that are not brackets from expr
    void clear_expr() {
        std::string filtered;
        for (char c : expr) {
            if (left_brackets.find(c) != std::string::npos ||
                right_brackets.find(c) != std::string::npos) {
                filtered.push_back(c);
            }
        }
        expr = filtered;
    }

    // Checks if the expression has balanced brackets
    bool check_balanced_brackets() {
        clear_expr();
        stack.clear();  // ensure a fresh start

        for (char brkt : expr) {
            if (left_brackets.find(brkt) != std::string::npos) {
                // Left bracket – push onto stack
                stack.push_back(brkt);
            } else {
                // Right bracket – must match the top of stack
                if (stack.empty()) return false;
                char current_brkt = stack.back();
                stack.pop_back();

                // Check matching
                if (current_brkt == '(' && brkt != ')') return false;
                if (current_brkt == '{' && brkt != '}') return false;
                if (current_brkt == '[' && brkt != ']') return false;
            }
        }

        // Stack must be empty for balanced brackets
        return stack.empty();
    }
};