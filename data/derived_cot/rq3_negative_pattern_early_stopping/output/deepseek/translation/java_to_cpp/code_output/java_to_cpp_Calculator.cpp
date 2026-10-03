#include <iostream>
#include <string>
#include <stack>
#include <map>
#include <cmath>
#include <functional>
#include <cctype>
#include <optional>

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
            if (std::isdigit(ch) || ch == '.') {
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
    std::map<char, std::function<double(double, double)>> operators;

    int precedence(char op) const {
        switch (op) {
            case '+':
            case '-': return 1;
            case '*':
            case '/': return 2;
            case '^': return 3;
            default: return 0;
        }
    }

    void applyOperator(std::stack<double>& operandStack, std::stack<char>& operatorStack) {
        char op = operatorStack.top(); operatorStack.pop();
        double right = operandStack.top(); operandStack.pop();
        double left = operandStack.top(); operandStack.pop();
        double result = operators[op](left, right);
        operandStack.push(result);
    }
};

int main() {
    Calculator calculator;
    auto result = calculator.calculate("1+2-3");
    if (result) {
        std::cout << *result << std::endl;
    } else {
        std::cout << "null" << std::endl;
    }
    return 0;
}