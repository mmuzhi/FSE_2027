#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstdlib>
#include <deque>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

/*
 * This is a class that can perform calculations with basic arithmetic
 * operations, including addition, subtraction, multiplication, division,
 * and modulo.
 */
class ExpressionCalculator {
public:
    ExpressionCalculator() {
        // Indexed by (char code - 40): '(' ')' '*' '+' ',' '-' '.' '/'
        static const int priority[8] = {0, 3, 2, 1, -1, 1, 0, 2};
        for (int i = 0; i < 8; ++i) operat_priority[i] = priority[i];
    }

    /*
     * Calculate the result of the given expression.
     * :param expression: string, the expression to be calculated
     * :return: double, the calculated result
     */
    double calculate(const std::string& expression) {
        prepare(transform(expression));

        std::deque<std::string> result_stack;
        std::reverse(postfix_stack.begin(), postfix_stack.end());

        while (!postfix_stack.empty()) {
            std::string current_op = pop_back_or_throw(postfix_stack);
            if (!is_operator(current_op)) {
                replace_all(current_op, '~', '-');
                result_stack.push_back(current_op);
            } else {
                std::string second_value = pop_back_or_throw(result_stack);
                std::string first_value = pop_back_or_throw(result_stack);

                replace_all(first_value, '~', '-');
                replace_all(second_value, '~', '-');

                long double temp_result = _calculate(first_value, second_value, current_op);
                result_stack.push_back(format_number(temp_result));
            }
        }

        // Equivalent of: float(eval("*".join(result_stack)))
        if (result_stack.empty()) {
            throw std::runtime_error("SyntaxError: unexpected EOF while parsing");
        }
        long double result = parse_number(result_stack.front());
        for (std::size_t i = 1; i < result_stack.size(); ++i) {
            result *= parse_number(result_stack[i]);
        }
        return static_cast<double>(result);
    }

    /*
     * Prepare the infix expression for conversion to postfix notation.
     * Tokens are appended to postfix_stack (it is not cleared here, matching
     * the Python original; calculate() drains it).
     */
    void prepare(const std::string& expression) {
        std::deque<std::string> op_stack;
        op_stack.push_back(",");
        std::vector<char> arr(expression.begin(), expression.end());
        std::size_t current_index = 0;
        std::size_t count = 0;

        for (std::size_t i = 0; i < arr.size(); ++i) {
            std::string current_op(1, arr[i]);
            if (is_operator(current_op)) {
                if (count > 0) {
                    postfix_stack.push_back(std::string(arr.begin() + current_index,
                                                        arr.begin() + current_index + count));
                }
                std::string peek_op = op_stack.back();
                if (current_op == ")") {
                    while (op_stack.back() != "(") {
                        postfix_stack.push_back(op_stack.back());
                        op_stack.pop_back();
                        if (op_stack.empty()) {
                            throw std::runtime_error("IndexError: pop from an empty deque");
                        }
                    }
                    op_stack.pop_back();
                } else {
                    while (current_op != "(" && peek_op != "," &&
                           compare(current_op, peek_op)) {
                        postfix_stack.push_back(op_stack.back());
                        op_stack.pop_back();
                        peek_op = op_stack.back();
                    }
                    op_stack.push_back(current_op);
                }

                count = 0;
                current_index = i + 1;
            } else {
                count += 1;
            }
        }

        if (count > 1 ||
            (count == 1 && !is_operator(std::string(1, arr[current_index])))) {
            postfix_stack.push_back(std::string(arr.begin() + current_index,
                                                arr.begin() + current_index + count));
        }

        while (op_stack.back() != ",") {
            postfix_stack.push_back(op_stack.back());
            op_stack.pop_back();
        }
    }

    /*
     * Check if a character is an operator in {'+', '-', '*', '/', '(', ')', '%'}
     */
    static bool is_operator(const std::string& c) {
        return c == "+" || c == "-" || c == "*" || c == "/" ||
               c == "(" || c == ")" || c == "%";
    }

    /*
     * Compare the precedence of two operators: True if the operator on top of
     * the stack has higher or equal precedence than the current one.
     */
    bool compare(const std::string& cur, const std::string& peek) const {
        char c = cur[0];
        char p = peek[0];
        if (c == '%') c = '/';
        if (p == '%') p = '/';
        return operat_priority[static_cast<int>(p) - 40] >=
               operat_priority[static_cast<int>(c) - 40];
    }

    /*
     * Perform the mathematical calculation based on the given operands and
     * operator. Python's decimal semantics are approximated with long double
     * (including truncated remainder, i.e. std::fmod, sign of the dividend).
     */
    static long double _calculate(const std::string& first_value,
                                  const std::string& second_value,
                                  const std::string& current_op) {
        long double first = parse_number(first_value);
        long double second = parse_number(second_value);
        if (current_op == "+") {
            return first + second;
        } else if (current_op == "-") {
            return first - second;
        } else if (current_op == "*") {
            return first * second;
        } else if (current_op == "/") {
            if (second == 0.0L) {
                throw std::runtime_error("decimal.DivisionByZero");
            }
            return first / second;
        } else if (current_op == "%") {
            if (second == 0.0L) {
                throw std::runtime_error("decimal.DivisionByZero");
            }
            return std::fmod(first, second);
        } else {
            throw std::invalid_argument("Unexpected operator: " + current_op);
        }
    }

    /*
     * Transform the infix expression to a format suitable for conversion:
     * strips whitespace and a trailing '=', marks unary minus as '~'.
     */
    static std::string transform(const std::string& expression) {
        // re.sub(r"\s+", "", expression)
        std::string expr;
        for (std::string::size_type i = 0; i < expression.size(); ++i) {
            char c = expression[i];
            if (!std::isspace(static_cast<unsigned char>(c))) {
                expr += c;
            }
        }
        // re.sub(r"=$", "", expression)
        if (!expr.empty() && expr[expr.size() - 1] == '=') {
            expr.erase(expr.size() - 1);
        }

        std::vector<char> arr(expr.begin(), expr.end());
        for (std::size_t i = 0; i < arr.size(); ++i) {
            if (arr[i] == '-') {
                if (i == 0) {
                    arr[i] = '~';
                } else {
                    char prev_c = arr[i - 1];
                    if (prev_c == '+' || prev_c == '-' || prev_c == '*' ||
                        prev_c == '/' || prev_c == '(' || prev_c == 'E' ||
                        prev_c == 'e') {
                        arr[i] = '~';
                    }
                }
            }
        }

        if (arr.empty()) {
            // Python: arr[0] raises IndexError on an empty expression.
            throw std::runtime_error("IndexError: list index out of range");
        }

        if (arr[0] == '~' && arr.size() > 1 && arr[1] == '(') {
            arr[0] = '-';
            return "0" + std::string(arr.begin(), arr.end());
        }
        return std::string(arr.begin(), arr.end());
    }

private:
    std::deque<std::string> postfix_stack;
    int operat_priority[8];

    // deque.pop() in Python pops from the right and raises IndexError if empty.
    static std::string pop_back_or_throw(std::deque<std::string>& stack) {
        if (stack.empty()) {
            throw std::runtime_error("IndexError: pop from an empty deque");
        }
        std::string value = stack.back();
        stack.pop_back();
        return value;
    }

    // str.replace("~", "-") for single characters.
    static void replace_all(std::string& s, char from, char to) {
        for (std::string::size_type i = 0; i < s.size(); ++i) {
            if (s[i] == from) s[i] = to;
        }
    }

    // Decimal(str) analogue; raises on non-numeric input like Decimal would.
    static long double parse_number(const std::string& s) {
        const char* cstr = s.c_str();
        char* end = nullptr;
        long double value = std::strtold(cstr, &end);
        if (end == cstr) {
            throw std::invalid_argument("InvalidOperation: " + s);
        }
        return value;
    }

    // Round-trip-safe str(Decimal(...)) analogue (Python float == C++ double).
    static std::string format_number(long double value) {
        std::ostringstream oss;
        oss.precision(std::numeric_limits<long double>::max_digits10);
        oss << value;
        return oss.str();
    }
};