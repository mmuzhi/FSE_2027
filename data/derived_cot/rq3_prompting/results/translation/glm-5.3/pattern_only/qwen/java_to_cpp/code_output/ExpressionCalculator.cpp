#include <cmath>
#include <deque>
#include <stdexcept>
#include <string>

class ExpressionCalculator {
public:
    std::deque<std::string> postfixStack;

    ExpressionCalculator() = default;

    double calculate(const std::string& expression) {
        std::string transformedExpression = transform(expression);
        prepare(transformedExpression);
        return evaluatePostfix();
    }

    void prepare(const std::string& expression) {
        postfixStack.clear();
        std::deque<char> operatorStack;
        const std::size_t length = expression.length();
        for (std::size_t i = 0; i < length; i++) {
            char ch = expression[i];
            if (isDigitChar(ch) || ch == '.') {
                std::string num;
                while (i < length && (isDigitChar(expression[i]) || expression[i] == '.')) {
                    num += expression[i++];
                }
                i--;
                postfixStack.push_back(num);
            } else if (ch == '(') {
                operatorStack.push_back(ch);
            } else if (ch == ')') {
                while (!operatorStack.empty() && operatorStack.back() != '(') {
                    postfixStack.push_back(std::string(1, operatorStack.back()));
                    operatorStack.pop_back();
                }
                operatorStack.pop_back();
            } else if (isOperator(ch)) {
                while (!operatorStack.empty() && isOperator(operatorStack.back()) &&
                       !compare(operatorStack.back(), ch)) {
                    postfixStack.push_back(std::string(1, operatorStack.back()));
                    operatorStack.pop_back();
                }
                operatorStack.push_back(ch);
            }
        }
        while (!operatorStack.empty()) {
            postfixStack.push_back(std::string(1, operatorStack.back()));
            operatorStack.pop_back();
        }
    }

    bool isOperator(char ch) const {
        return ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '%';
    }

    bool compare(char op1, char op2) const {
        char cur_op = (op1 == '%') ? '/' : op1;
        char peek_op = (op2 == '%') ? '/' : op2;
        static const int operat_priority[] = {0, 3, 2, 1, -1, 1, 0, 2};
        return operat_priority[peek_op - 40] >= operat_priority[cur_op - 40];
    }

    std::string transform(std::string expression) {
        // expression.replaceAll(" ", "")
        std::string noSpaces;
        for (char c : expression) {
            if (c != ' ') noSpaces += c;
        }
        expression = noSpaces;
        // expression.replaceAll("-", "~")
        for (char& c : expression) {
            if (c == '-') c = '~';
        }
        if (!expression.empty() && expression[0] == '~' && expression.length() > 1 &&
            expression[1] == '(') {
            expression[0] = '-';
            return "0" + expression;
        }
        return expression;
    }

    double _calculate(double a, double b, char op) const {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            case '%': return std::fmod(a, b);  // Java's double % semantics
            default:
                throw std::invalid_argument("Unsupported operator: " + std::string(1, op));
        }
    }

private:
    static bool isDigitChar(char c) {
        return c >= '0' && c <= '9';
    }

    double evaluatePostfix() {
        std::deque<double> stack;
        for (const std::string& token : postfixStack) {
            if (isOperator(token[0])) {
                double b = stack.back();
                stack.pop_back();
                double a = stack.back();
                stack.pop_back();
                stack.push_back(_calculate(a, b, token[0]));
            } else {
                stack.push_back(std::stod(token));
            }
        }
        return stack.back();
    }
};