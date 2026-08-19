#include <cctype>
#include <cmath>
#include <functional>
#include <map>
#include <optional>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class Calculator {
public:
    Calculator() : operators_{
        {'+', [](double x, double y) { return x + y; }},
        {'-', [](double x, double y) { return x - y; }},
        {'*', [](double x, double y) { return x * y; }},
        {'/', [](double x, double y) {
             if (y == 0.0) throw std::runtime_error("float division by zero");  // ZeroDivisionError
             return x / y;
         }},
        {'^', [](double x, double y) {
             if (x == 0.0 && y < 0.0)
                 throw std::runtime_error("0.0 cannot be raised to a negative power");  // ZeroDivisionError
             return std::pow(x, y);
         }},
    } {}

    // Calculate the value of a given expression.
    // Returns the value of the expression, or std::nullopt (Python None) if none.
    std::optional<double> calculate(const std::string& expression) {
        std::vector<double> operand_stack;
        std::vector<char> operator_stack;
        std::string num_buffer;

        for (char ch : expression) {
            if (std::isdigit(static_cast<unsigned char>(ch)) || ch == '.') {
                num_buffer += ch;
            } else {
                if (!num_buffer.empty()) {
                    operand_stack.push_back(parse_float(num_buffer));
                    num_buffer.clear();
                }

                if (ch == '+' || ch == '-' || ch == '*' || ch == '/' || ch == '^') {
                    while (!operator_stack.empty() &&
                           operator_stack.back() != '(' &&
                           precedence(operator_stack.back()) >= precedence(ch)) {
                        apply_operator(operand_stack, operator_stack);
                    }
                    operator_stack.push_back(ch);
                } else if (ch == '(') {
                    operator_stack.push_back(ch);
                } else if (ch == ')') {
                    while (!operator_stack.empty() && operator_stack.back() != '(') {
                        apply_operator(operand_stack, operator_stack);
                    }
                    pop_or_throw(operator_stack);
                }
                // Any other character is ignored, matching the Python code.
            }
        }

        if (!num_buffer.empty()) {
            operand_stack.push_back(parse_float(num_buffer));
        }

        while (!operator_stack.empty()) {
            apply_operator(operand_stack, operator_stack);
        }

        return operand_stack.empty() ? std::nullopt
                                     : std::optional<double>(operand_stack.back());
    }

    // Returns the priority of the given operator; 0 for unknown operators.
    int precedence(char op) const {
        static const std::map<char, int> precedences{
            {'+', 1}, {'-', 1}, {'*', 2}, {'/', 2}, {'^', 3}};
        auto it = precedences.find(op);
        return it == precedences.end() ? 0 : it->second;
    }

    // Applies the operator on top of operator_stack to the two top operands.
    std::pair<std::vector<double>, std::vector<char>>
    apply_operator(std::vector<double>& operand_stack, std::vector<char>& operator_stack) {
        char op = pop_or_throw(operator_stack);
        double operand2 = pop_or_throw(operand_stack);
        double operand1 = pop_or_throw(operand_stack);
        // .at() throws std::out_of_range for '(' etc., mirroring Python's KeyError.
        double result = operators_.at(op)(operand1, operand2);
        operand_stack.push_back(result);
        return {operand_stack, operator_stack};
    }

private:
    std::map<char, std::function<double(double, double)>> operators_;

    // Mirrors list.pop() on an empty list -> IndexError.
    template <typename T>
    static T pop_or_throw(std::vector<T>& v) {
        if (v.empty()) throw std::out_of_range("pop from empty list");
        T value = v.back();
        v.pop_back();
        return value;
    }

    // Mirrors Python float(buffer) for a buffer containing only digits and '.':
    // raises std::invalid_argument (Python ValueError) on malformed input such
    // as "." or "1.2.3", and yields infinity on overflow like Python's float().
    static double parse_float(const std::string& buffer) {
        std::size_t dots = 0;
        bool has_digit = false;
        for (char c : buffer) {
            if (c == '.') ++dots;
            else has_digit = true;
        }
        if (dots > 1 || !has_digit)
            throw std::invalid_argument(
                "could not convert string to float: '" + buffer + "'");
        try {
            return std::stod(buffer);
        } catch (const std::out_of_range&) {
            return HUGE_VAL;  // buffer never contains '-', so overflow is positive
        }
    }
};