#include <cctype>
#include <cmath>
#include <cstdlib>
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
        const int length = static_cast<int>(expression.length());
        for (int i = 0; i < length; i++) {
            char ch = expression[i];
            if (std::isdigit(static_cast<unsigned char>(ch)) || ch == '.') {
                std::string num;
                while (i < length && (std::isdigit(static_cast<unsigned char>(expression[i])) || expression[i] == '.')) {
                    num += expression[i++];
                }
                i--;
                postfixStack.push_back(num); // ArrayDeque.add -> tail (FIFO)
            } else if (ch == '(') {
                operatorStack.push_front(ch); // push -> head (LIFO)
            } else if (ch == ')') {
                while (!operatorStack.empty() && operatorStack.front() != '(') {
                    postfixStack.push_back(std::string(1, operatorStack.front()));
                    operatorStack.pop_front();
                }
                operatorStack.pop_front();
            } else if (isOperator(ch)) {
                while (!operatorStack.empty() && isOperator(operatorStack.front()) &&
                       !compare(operatorStack.front(), ch)) {
                    postfixStack.push_back(std::string(1, operatorStack.front()));
                    operatorStack.pop_front();
                }
                operatorStack.push_front(ch);
            }
        }
        while (!operatorStack.empty()) {
            postfixStack.push_back(std::string(1, operatorStack.front()));
            operatorStack.pop_front();
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

    std::string transform(std::string expression) {
        // replaceAll(" ", "")
        std::string noSpaces;
        noSpaces.reserve(expression.size());
        for (char c : expression) {
            if (c != ' ') noSpaces += c;
        }
        // replaceAll("-", "~")
        for (char& c : noSpaces) {
            if (c == '-') c = '~';
        }
        // chars[0] on an empty array throws in Java; .at() mirrors that.
        if (noSpaces.at(0) == '~' && noSpaces.length() > 1 && noSpaces.at(1) == '(') {
            noSpaces[0] = '-';
            return "0" + noSpaces;
        } else {
            return noSpaces;
        }
    }

private:
    double evaluatePostfix() {
        std::deque<double> stack;
        for (const std::string& token : postfixStack) { // ArrayDeque iteration: head -> tail
            if (isOperator(token[0])) {
                double b = stack.front(); stack.pop_front();
                double a = stack.front(); stack.pop_front();
                stack.push_front(_calculate(a, b, token[0]));
            } else {
                stack.push_front(parseDouble(token));
            }
        }
        double result = stack.front(); stack.pop_front();
        return result;
    }

    double _calculate(double a, double b, char oper) {
        switch (oper) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            case '%': return std::fmod(a, b); // Java's double % has fmod semantics
            default:
                throw std::invalid_argument("Unsupported operator: " + std::string(1, oper));
        }
    }

    // Mirrors Double.parseDouble: rejects partial parses, returns +-HUGE_VAL on overflow.
    static double parseDouble(const std::string& s) {
        const char* cstr = s.c_str();
        char* end = nullptr;
        double value = std::strtod(cstr, &end);
        if (end == cstr || static_cast<std::size_t>(end - cstr) != s.size()) {
            throw std::invalid_argument("For input string: \"" + s + "\"");
        }
        return value;
    }
};