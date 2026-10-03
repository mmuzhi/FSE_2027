#include <string>
#include <deque>
#include <stack>
#include <cctype>
#include <cmath>
#include <stdexcept>
#include <algorithm>

class ExpressionCalculator {
private:
    std::deque<std::string> postfixStack;

    bool isOperator(char ch) const {
        return ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '%';
    }

    // Returns true if op2 has priority >= op1 priority (used in shunting-yard)
    bool compare(char op1, char op2) const {
        char cur_op = (op1 == '%') ? '/' : op1;
        char peek_op = (op2 == '%') ? '/' : op2;
        // priorities for chars around 40..47
        int operat_priority[8] = {0, 3, 2, 1, -1, 1, 0, 2};
        return operat_priority[peek_op - 40] >= operat_priority[cur_op - 40];
    }

    double _calculate(double a, double b, char op) const {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            case '%': return std::fmod(a, b);
            default: throw std::invalid_argument("Unsupported operator: " + std::string(1, op));
        }
    }

    double evaluatePostfix() {
        std::stack<double> stack;
        for (const std::string& token : postfixStack) {
            if (token.length() == 1 && isOperator(token[0])) {
                double b = stack.top(); stack.pop();
                double a = stack.top(); stack.pop();
                stack.push(_calculate(a, b, token[0]));
            } else {
                stack.push(std::stod(token));
            }
        }
        double result = stack.top();
        stack.pop();
        return result;
    }

public:
    ExpressionCalculator() = default;

    double calculate(const std::string& expression) {
        std::string transformed = transform(expression);
        prepare(transformed);
        return evaluatePostfix();
    }

    void prepare(const std::string& expression) {
        postfixStack.clear();
        std::stack<char> operatorStack;
        size_t length = expression.length();
        for (size_t i = 0; i < length; ++i) {
            char ch = expression[i];
            if (std::isdigit(ch) || ch == '.') {
                std::string num;
                while (i < length && (std::isdigit(expression[i]) || expression[i] == '.')) {
                    num += expression[i++];
                }
                --i;
                postfixStack.push_back(num);
            } else if (ch == '(') {
                operatorStack.push(ch);
            } else if (ch == ')') {
                while (!operatorStack.empty() && operatorStack.top() != '(') {
                    postfixStack.push_back(std::string(1, operatorStack.top()));
                    operatorStack.pop();
                }
                operatorStack.pop();  // pop '('
            } else if (isOperator(ch)) {
                while (!operatorStack.empty() && isOperator(operatorStack.top()) && !compare(operatorStack.top(), ch)) {
                    postfixStack.push_back(std::string(1, operatorStack.top()));
                    operatorStack.pop();
                }
                operatorStack.push(ch);
            }
        }
        while (!operatorStack.empty()) {
            postfixStack.push_back(std::string(1, operatorStack.top()));
            operatorStack.pop();
        }
    }

    std::string transform(std::string expression) {
        // Remove all spaces
        expression.erase(std::remove(expression.begin(), expression.end(), ' '), expression.end());
        // Replace all '-' with '~'
        std::replace(expression.begin(), expression.end(), '-', '~');
        // Handle leading unary minus before '('
        if (!expression.empty() && expression[0] == '~' && expression.length() > 1 && expression[1] == '(') {
            expression[0] = '-';
            return "0" + expression;
        }
        return expression;
    }
};