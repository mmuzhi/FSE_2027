#include <algorithm>
#include <cerrno>
#include <cmath>
#include <cstdlib>
#include <deque>
#include <stack>
#include <stdexcept>
#include <string>

class ExpressionCalculator {
public:
    ExpressionCalculator() = default;

    double calculate(const std::string& expression) {
        std::string transformedExpression = transform(expression);
        prepare(transformedExpression);
        return evaluatePostfix();
    }

    void prepare(const std::string& expression) {
        postfixStack.clear();
        std::stack<char> operatorStack; // Java ArrayDeque used as LIFO (push/pop/peek)
        int length = static_cast<int>(expression.length());
        for (int i = 0; i < length; i++) {
            char ch = expression[i];
            if (isDigitChar(ch) || ch == '.') {
                std::string num;
                while (i < length && (isDigitChar(expression[i]) || expression[i] == '.')) {
                    num += expression[i++];
                }
                i--;
                postfixStack.push_back(num); // Deque.add == addLast
            } else if (ch == '(') {
                operatorStack.push(ch);
            } else if (ch == ')') {
                while (!operatorStack.empty() && operatorStack.top() != '(') {
                    postfixStack.push_back(std::string(1, operatorStack.top()));
                    operatorStack.pop();
                }
                if (operatorStack.empty()) {
                    // Java ArrayDeque.pop() on empty throws NoSuchElementException
                    throw std::runtime_error("NoSuchElementException");
                }
                operatorStack.pop();
            } else if (isOperator(ch)) {
                while (!operatorStack.empty() && isOperator(operatorStack.top()) &&
                       !compare(operatorStack.top(), ch)) {
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
        static const int operat_priority[] = {0, 3, 2, 1, -1, 1, 0, 2};
        return operat_priority[peek_op - 40] >= operat_priority[cur_op - 40];
    }

    double _calculate(double a, double b, char op) {
        switch (op) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            case '%': return std::fmod(a, b); // Java % on doubles == fmod semantics
            default:  throw std::invalid_argument("Unsupported operator: " + std::string(1, op));
        }
    }

    std::string transform(std::string expression) {
        expression.erase(std::remove(expression.begin(), expression.end(), ' '), expression.end());
        std::replace(expression.begin(), expression.end(), '-', '~');
        if (expression.empty()) {
            // Java: chars[0] on empty array throws ArrayIndexOutOfBoundsException
            throw std::out_of_range("ArrayIndexOutOfBoundsException: Index 0 out of bounds for length 0");
        }
        if (expression[0] == '~' && expression.length() > 1 && expression[1] == '(') {
            expression[0] = '-';
            return "0" + expression;
        } else {
            return expression;
        }
    }

private:
    static bool isDigitChar(char c) {
        return c >= '0' && c <= '9';
    }

    // Mirrors Java Double.parseDouble for digit/dot tokens:
    // rejects partially-parsed input (e.g. "1.2.3", "."), returns ±inf on overflow.
    static double parseDouble(const std::string& s) {
        size_t pos = 0;
        try {
            double v = std::stod(s, &pos);
            if (pos != s.size()) {
                throw std::invalid_argument("NumberFormatException: " + s);
            }
            return v;
        } catch (const std::out_of_range&) {
            errno = 0;
            return std::strtod(s.c_str(), nullptr); // ±HUGE_VAL, like Java's Infinity
        }
    }

    static double popDouble(std::stack<double>& s) {
        if (s.empty()) {
            throw std::runtime_error("NoSuchElementException");
        }
        double v = s.top();
        s.pop();
        return v;
    }

    double evaluatePostfix() {
        std::stack<double> stack;
        for (const std::string& token : postfixStack) { // ArrayDeque iterates head->tail == insertion order
            if (isOperator(token[0])) {
                double b = popDouble(stack);
                double a = popDouble(stack);
                stack.push(_calculate(a, b, token[0]));
            } else {
                stack.push(parseDouble(token));
            }
        }
        return popDouble(stack);
    }

    std::deque<std::string> postfixStack;
};