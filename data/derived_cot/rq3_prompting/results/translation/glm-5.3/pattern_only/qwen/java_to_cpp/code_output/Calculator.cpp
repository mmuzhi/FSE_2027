#include <cctype>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <functional>
#include <iostream>
#include <limits>
#include <optional>
#include <stack>
#include <string>
#include <unordered_map>

class Calculator {
private:
    std::unordered_map<char, std::function<double(double, double)>> operators;

public:
    Calculator() {
        operators['+'] = [](double x, double y) { return x + y; };
        operators['-'] = [](double x, double y) { return x - y; };
        operators['*'] = [](double x, double y) { return x * y; };
        operators['/'] = [](double x, double y) { return x / y; };
        operators['^'] = [](double x, double y) { return std::pow(x, y); };
    }

    // Returns std::nullopt where the Java version returns null.
    std::optional<double> calculate(const std::string& expression) {
        std::stack<double> operandStack;
        std::stack<char> operatorStack;
        std::string numBuffer;

        for (size_t i = 0; i < expression.length(); i++) {
            char ch = expression[i];
            if (std::isdigit(static_cast<unsigned char>(ch)) || ch == '.') {
                numBuffer += ch;
            } else {
                if (!numBuffer.empty()) {
                    operandStack.push(std::stod(numBuffer));
                    numBuffer.clear();
                }

                if (operators.find(ch) != operators.end()) {
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
                    operatorStack.pop();
                }
            }
        }

        if (!numBuffer.empty()) {
            operandStack.push(std::stod(numBuffer));
        }

        while (!operatorStack.empty()) {
            applyOperator(operandStack, operatorStack);
        }

        if (operandStack.empty()) {
            return std::nullopt;
        }
        return operandStack.top();
    }

private:
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

    void applyOperator(std::stack<double>& operandStack, std::stack<char>& operatorStack) {
        char op = operatorStack.top();
        operatorStack.pop();
        double operand2 = operandStack.top();
        operandStack.pop();
        double operand1 = operandStack.top();
        operandStack.pop();
        double result = operators.at(op)(operand1, operand2);
        operandStack.push(result);
    }
};

// Mimics Java's Double.toString / System.out.println(Double) formatting
// (shortest round-trip form, always a '.' or exponent, 'E' exponent notation).
static std::string javaDoubleToString(double value) {
    if (std::isnan(value)) return "NaN";
    if (value == std::numeric_limits<double>::infinity()) return "Infinity";
    if (value == -std::numeric_limits<double>::infinity()) return "-Infinity";

    char buf[64];
    for (int precision = 1; precision <= 17; ++precision) {
        std::snprintf(buf, sizeof(buf), "%.*g", precision, value);
        if (std::strtod(buf, nullptr) == value) break;
    }
    std::string s(buf);

    size_t ePos = s.find('e');
    if (ePos != std::string::npos) {
        std::string mantissa = s.substr(0, ePos);
        std::string exponent = s.substr(ePos + 1);
        if (mantissa.find('.') == std::string::npos) mantissa += ".0";
        if (!exponent.empty() && exponent[0] == '+') exponent.erase(0, 1);
        s = mantissa + "E" + exponent;
    } else if (s.find('.') == std::string::npos) {
        s += ".0";
    }
    return s;
}

int main() {
    Calculator calculator;
    std::optional<double> result = calculator.calculate("1+2-3");
    if (result.has_value()) {
        std::cout << javaDoubleToString(*result) << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }
    return 0;
}