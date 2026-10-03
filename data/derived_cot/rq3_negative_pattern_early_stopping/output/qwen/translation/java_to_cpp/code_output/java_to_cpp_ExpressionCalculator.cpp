#include <iostream>
#include <string>
#include <deque>
#include <stack>
#include <cctype>
#include <algorithm>
#include <map>

class ExpressionCalculator {
private:
    std::deque<std::string> postfixStack;

    bool isOperator(char ch) {
        return ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '%';
    }

    int getOperatorPriority(char op) {
        static const std::map<char, int> priorityMap = {{'+', 1}, 
                                                       {'-', 1}, 
                                                       {'*', 2}, 
                                                       {'/', 2}, 
                                                       {'%', 2}};
        return priorityMap.at(op);
    }

    bool compare(char op1, char op2) {
        int p1 = (op1 == '%') ? getOperatorPriority('/') : getOperatorPriority(op1);
        int p2 = (op2 == '%') ? getOperatorPriority('/') : getOperatorPriority(op2);
        return p1 >= p2;
    }

    double _calculate(double a, double b, char operator) {
        switch (operator) {
            case '+': return a + b;
            case '-': return a - b;
            case '*': return a * b;
            case '/': return a / b;
            case '%': return std::fmod(a, b);
            default: throw std::invalid_argument("Unsupported operator: " + std::string(1, operator));
        }
    }

    std::string transform(const std::string& expression) {
        std::string expr = expression;
        // Remove spaces
        expr.erase(std::remove_if(expr.begin(), expr.end(), [](unsigned char ch) { return std::isspace(ch); }), expr.end());
        // Replace '-' with '~'
        std::replace_if(expr.begin(), expr.end(), [](unsigned char ch) { return ch == '-'; }, '~');
        // Handle negative numbers in parentheses
        if (!expr.empty() && expr[0] == '~' && expr.length() > 1 && expr[1] == '(') {
            expr[0] = '-';
            expr = '0' + expr;
        }
        return expr;
    }

public:
    ExpressionCalculator() = default;

    double calculate(const std::string& expression) {
        std::string transformedExpr = transform(expression);
        prepare(transformedExpr);
        return evaluatePostfix();
    }

    void prepare(const std::string& expression) {
        postfixStack.clear();
        std::stack<char> operatorStack;
        int length = expression.length();
        for (int i = 0; i < length; i++) {
            char ch = expression[i];
            if (std::isdigit(ch) || ch == '.') {
                std::string num;
                while (i < length && (std::isdigit(expression[i]) || expression[i] == '.')) {
                    num += expression[i];
                    i++;
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
                if (!operatorStack.empty()) operatorStack.pop();
            } else if (isOperator(ch)) {
                while (!operatorStack.empty() && isOperator(operatorStack.top()) && compare(operatorStack.top(), ch)) {
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

    double evaluatePostfix() {
        std::deque<double> evalStack;
        for (const auto& token : postfixStack) {
            if (isOperator(token[0])) {
                double b = evalStack.back(); evalStack.pop_back();
                double a = evalStack.back(); evalStack.pop_back();
                evalStack.push_back(_calculate(a, b, token[0]));
            } else {
                evalStack.push_back(std::stod(token));
            }
        }
        return evalStack.back();
    }
};