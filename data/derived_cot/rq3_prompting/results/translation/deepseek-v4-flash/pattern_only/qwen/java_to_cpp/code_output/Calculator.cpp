#include <cctype>
#include <charconv>
#include <cmath>
#include <functional>
#include <iostream>
#include <optional>
#include <stack>
#include <stdexcept>
#include <string>
#include <system_error>
#include <unordered_map>

class Calculator {
public:
    Calculator() {
        operators['+'] = [](double x, double y) { return x + y; };
        operators['-'] = [](double x, double y) { return x - y; };
        operators['*'] = [](double x, double y) { return x * y; };
        operators['/'] = [](double x, double y) { return x / y; };
        operators['^'] = [](double x, double y) { return std::pow(x, y); };
    }

    std::optional<double> calculate(const std::string& expression) {
        std::stack<double> operandStack;
        std::stack<char> operatorStack;
        std::string numBuffer;

        for (size_t i = 0; i < expression.length(); ++i) {
            char ch = expression[i];
            if (std::isdigit(static_cast<unsigned char>(ch)) || ch == '.') {
                numBuffer.push_back(ch);
            } else {
                if (!numBuffer.empty()) {
                    operandStack.push(parseNumber(numBuffer));
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
                    if (operatorStack.empty()) {
                        throw std::runtime_error("EmptyStackException");
                    }
                    operatorStack.pop();
                }
            }
        }

        if (!numBuffer.empty()) {
            operandStack.push(parseNumber(numBuffer));
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
    std::unordered_map<char, std::function<double(double, double)>> operators;

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
        if (operatorStack.empty()) {
            throw std::runtime_error("EmptyStackException");
        }
        char op = operatorStack.top();
        operatorStack.pop();

        if (operandStack.size() < 2) {
            throw std::runtime_error("EmptyStackException");
        }
        double operand2 = operandStack.top();
        operandStack.pop();
        double operand1 = operandStack.top();
        operandStack.pop();

        double result = operators.at(op)(operand1, operand2);
        operandStack.push(result);
    }

    static double parseNumber(const std::string& s) {
        size_t idx = 0;
        double value = std::stod(s, &idx);
        if (idx != s.length()) {
            throw std::invalid_argument("NumberFormatException");
        }
        return value;
    }
};

std::string javaDoubleToString(double value) {
    if (std::isnan(value)) return "NaN";
    if (std::isinf(value)) return value > 0 ? "Infinity" : "-Infinity";
    if (value == 0.0) return std::signbit(value) ? "-0.0" : "0.0";

    char buf[128];
    auto res = std::to_chars(buf, buf + sizeof(buf), value, std::chars_format::scientific);
    if (res.ec != std::errc()) {
        return "0.0";
    }
    std::string s(buf, res.ptr);

    std::string sign;
    if (!s.empty() && s[0] == '-') {
        sign = "-";
        s.erase(0, 1);
    }

    size_t epos = s.find('e');
    if (epos == std::string::npos) {
        return sign + s;
    }

    std::string mantissa = s.substr(0, epos);
    int exp = std::stoi(s.substr(epos + 1));

    std::string digits;
    for (char c : mantissa) {
        if (c != '.') {
            digits.push_back(c);
        }
    }

    if (exp >= 7 || exp < -3) {
        std::string result = sign;
        result.push_back(digits[0]);
        if (digits.size() == 1) {
            result += ".0";
        } else {
            result += ".";
            result += digits.substr(1);
        }
        result += "E";
        result += std::to_string(exp);
        return result;
    } else {
        int pos = exp + 1;
        std::string result = sign;
        if (pos <= 0) {
            result += "0.";
            result.append(-pos, '0');
            result += digits;
        } else if (pos < static_cast<int>(digits.size())) {
            result += digits.substr(0, pos);
            result += ".";
            result += digits.substr(pos);
        } else {
            result += digits;
            result.append(pos - static_cast<int>(digits.size()), '0');
            result += ".0";
        }
        return result;
    }
}

int main() {
    Calculator calculator;
    auto result = calculator.calculate("1+2-3");
    if (result.has_value()) {
        std::cout << javaDoubleToString(*result) << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }
    return 0;
}