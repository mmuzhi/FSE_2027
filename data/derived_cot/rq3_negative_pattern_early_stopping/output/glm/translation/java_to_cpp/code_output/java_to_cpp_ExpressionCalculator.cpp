#include <string>
#include <deque>
#include <stack>
#include <cmath>
#include <stdexcept>
#include <cctype>

class ExpressionCalculator {
public:
    std::deque<std::string> postfixStack;

    ExpressionCalculator() {}

    double calculate(const std::string& expression) {
        std::string transformedExpression = transform(expression);
        prepare(transformedExpression);
        return evaluatePostfix();
    }

    void prepare(const std::string& expression) {
        postfixStack.clear();
        std::stack<char> operatorStack;
        int length = static_cast<int>(expression.length());
        for (int i = 0; i < length; i++) {
            char ch = expression[i];
            if (std::isdigit(static_cast<unsigned char>(ch)) || ch == '.') {
                std::string num;
                while (i < length && (std::isdigit(static_cast<unsigned char>(expression[i])) || expression[i] == '.')) {
                    num += expression[i++];
                }
                i--;
                postfixStack.push_back(num);
            } else if (ch == '(') {
                operatorStack.push(ch);
            } else if (ch == ')') {
                while (!operatorStack.empty() && operatorStack.top() != '(') {
                    postfixStack.push_back(std::string(1, operatorStack.top()));
                    operatorStack.pop();
                }
                operatorStack.pop();
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

    bool isOperator(char ch) {
        return ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '%';
    }

    bool compare(char op1, char op2) {
        char cur_op = (op1 == '%') ? '/' : op1;
        char peek_op = (op2 == '%') ? '/' : op2;
        int operat_priority[] = {0, 3, 2, 1, -1, 1, 0, 2};
        return operat_priority[peek_op - 40] >= operat_priority[cur_op - 40];
    }

private:
    double evaluatePostfix() {
        std::stack<double> stack;
        for (const std::string& token : postfixStack) {
            if (isOperator(token[0])) {
                double b = stack.top(); stack.pop();
                double a = stack.top(); stack.pop();
                stack.push(_calculate(a, b, token[0]));
            } else {
                stack.push(std::stod(token));
            }
        }
        double result = stack.top(); stack.pop();
        return result;
    }

    double _calculate(double a, double b, char op) {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            case '%': return std::fmod(a, b);
            default: throw std::invalid_argument("Unsupported operator: " + std::string(1, op));
        }
    }

public:
    std::string transform(std::string expression) {
        // Remove spaces
        std::string noSpaces;
        for (char c : expression) {
            if (c != ' ') noSpaces += c;
        }
        expression = noSpaces;

        // Replace '-' with '~'
        for (char& c : expression) {
            if (c == '-') c = '~';
        }

        if (!expression.empty() && expression[0] == '~' && expression.length() > 1 && expression[1] == '(') {
            expression[0] = '-';
            return "0" + expression;
        } else {
            return expression;
        }
    }
};