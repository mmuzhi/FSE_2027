#include <iostream>
#include <stack>
#include <string>

class BalancedBrackets {
private:
    std::stack<char> stack;
    std::string leftBrackets;
    std::string rightBrackets;
    std::string expr;

public:
    BalancedBrackets(const std::string& expr)
        : stack(), leftBrackets("({["), rightBrackets(")}]"), expr(expr) {}

    void clearExpr() {
        std::string cleanedExpr;
        for (char c : expr) {
            if (leftBrackets.find(c) != std::string::npos ||
                rightBrackets.find(c) != std::string::npos) {
                cleanedExpr += c;
            }
        }
        expr = cleanedExpr;
    }

    bool checkBalancedBrackets() {
        clearExpr();
        for (char Brkt : expr) {
            if (leftBrackets.find(Brkt) != std::string::npos) {
                stack.push(Brkt);
            } else {
                if (stack.empty()) {
                    return false;
                }
                char currentBrkt = stack.top();
                stack.pop();
                if (currentBrkt == '(' && Brkt != ')') return false;
                if (currentBrkt == '{' && Brkt != '}') return false;
                if (currentBrkt == '[' && Brkt != ']') return false;
            }
        }
        return stack.empty();
    }

    std::string getExpr() const {
        return expr;
    }
};

int main() {
    BalancedBrackets b("a(b)c");
    std::cout << std::boolalpha << b.checkBalancedBrackets() << std::endl;
    return 0;
}