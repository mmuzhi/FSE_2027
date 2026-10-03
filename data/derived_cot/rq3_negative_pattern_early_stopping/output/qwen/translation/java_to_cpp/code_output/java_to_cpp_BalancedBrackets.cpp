#include <iostream>
#include <stack>
#include <string>
#include <map>

class BalancedBrackets {
private:
    std::stack<char> stack;
    std::string leftBrackets;
    std::string rightBrackets;
    std::string expr;

public:
    BalancedBrackets(const std::string& expr) : expr(expr) {
        leftBrackets = "({[";
        rightBrackets = ")}]";
    }

    void clearExpr() {
        std::string cleanedExpr = "";
        for (char c : expr) {
            if (leftBrackets.find(c) != std::string::npos || rightBrackets.find(c) != std::string::npos) {
                cleanedExpr += c;
            }
        }
        expr = cleanedExpr;
    }

    bool checkBalancedBrackets() {
        clearExpr();
        std::map<char, char> bracketMap;
        bracketMap[')'] = '(';
        bracketMap['}'] = '{';
        bracketMap[']'] = '[';

        for (char c : expr) {
            if (leftBrackets.find(c) != std::string::npos) {
                stack.push(c);
            } else {
                if (stack.empty()) {
                    return false;
                }
                char topChar = stack.top();
                stack.pop();
                if (bracketMap[c] != topChar) {
                    return false;
                }
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
    std::cout << (b.checkBalancedBrackets() ? "true" : "false") << std::endl;
    return 0;
}