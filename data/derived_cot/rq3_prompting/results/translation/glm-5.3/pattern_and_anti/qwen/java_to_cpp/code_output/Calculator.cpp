#include <cctype>
#include <cmath>
#include <functional>
#include <iostream>
#include <limits>
#include <optional>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <string>
#include <unordered_map>

// org.example.Calculator

class Calculator {
private:
    using Operation = std::function<double(double, double)>;
    std::unordered_map<char, Operation> operators;

    [[noreturn]] static void emptyStackException() {
        throw std::runtime_error("java.util.EmptyStackException");
    }

    // Mirrors Double.parseDouble for buffers consisting of digits and '.' only.
    static double parseDouble(const std::string& s) {
        std::size_t pos = 0;
        double value;
        try {
            value = std::stod(s, &pos);
        } catch (const std::out_of_range&) {
            // Java saturates overflow to infinity.
            return std::numeric_limits<double>::infinity();
        }
        if (pos != s.size()) {
            throw std::invalid_argument("NumberFormatException");
        }
        return value;
    }

public:
    Calculator() {
        operators.emplace('+', [](double x, double y) { return x + y; });
        operators.emplace('-', [](double x, double y) { return x - y; });
        operators.emplace('*', [](double x, double y) { return x * y; });
        operators.emplace('/', [](double x, double y) { return x / y; });
        operators.emplace('^', [](double x, double y) { return std::pow(x, y); });
    }

    // Mirrors Java's Double.toString / println(double) formatting.
    static std::string javaDoubleToString(double value) {
        std::ostringstream oss;
        oss << value;
        std::string s = oss.str();
        if (s.find_first_of(".eE") == std::string::npos) {
            s += ".0";
        }
        return s;
    }

    // Java returns Double (null when the operand stack ends up empty).
    std::optional<double> calculate(const std::string& expression) {
        std::stack<double> operandStack;
        std::stack<char> operatorStack;
        std::string numBuffer;

        for (std::size_t i = 0; i < expression.length(); i++) {
            char ch = expression[i];
            if (std::isdigit(static_cast<unsigned char>(ch)) || ch == '.') {
                numBuffer += ch;
            } else {
                if (!numBuffer.empty()) {
                    operandStack.push(parseDouble(numBuffer));
                    numBuffer.clear();
                }

                if (operators.count(ch) > 0) {
                    while (!operatorStack.empty() &&
                           operatorStack.top() != '(' &&
                           precedence(operatorStack.top()) >= precedence(ch)) {
                        applyOperator(operandStack, operatorStack);
                    }
                    operatorStack.push(ch);
                } else if (ch == '(') {
                    operatorStack.push(ch);
                } else if (ch == ')') {
                    while (!operatorStack.empty() && operatorStack.top() != '(') {
                        applyOperator(operandStack, operatorStack);
                    }
                    if (operatorStack.empty()) {
                        emptyStackException(); // Java: pop() on empty Stack
                    }
                    operatorStack.pop();
                }
            }
        }

        if (!numBuffer.empty()) {
            operandStack.push(parseDouble(numBuffer));
        }

        while (!operatorStack.empty()) {
            applyOperator(operandStack, operatorStack);
        }

        return operandStack.empty() ? std::nullopt
                                    : std::optional<double>(operandStack.top());
    }

    int precedence(char op) const {
        switch (op) {
            case '+':
            case '-':
                return 1;
            case '*':
            case '/':
                return 2;
            case '^':
                return 3;
            default:
                return 0;
        }
    }

    void applyOperator(std::stack<double>& operandStack,
                       std::stack<char>& operatorStack) {
        char op = operatorStack.top();
        operatorStack.pop();
        if (operandStack.size() < 2) {
            emptyStackException(); // Java: EmptyStackException on pop()
        }
        double operand2 = operandStack.top();
        operandStack.pop();
        double operand1 = operandStack.top();
        operandStack.pop();
        double result = operators.at(op)(operand1, operand2);
        operandStack.push(result);
    }
};

int main() {
    Calculator calculator;
    std::optional<double> result = calculator.calculate("1+2-3");
    if (result.has_value()) {
        std::cout << Calculator::javaDoubleToString(*result) << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }
    return 0;
}