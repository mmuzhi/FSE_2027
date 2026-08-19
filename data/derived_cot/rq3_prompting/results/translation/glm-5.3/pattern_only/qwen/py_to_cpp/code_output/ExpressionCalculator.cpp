#include <algorithm>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <deque>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

class ExpressionCalculator {
public:
    ExpressionCalculator() : operat_priority{0, 3, 2, 1, -1, 1, 0, 2} {}

    double calculate(const std::string& expression) {
        prepare(transform(expression));

        std::deque<std::string> result_stack;
        std::reverse(postfix_stack.begin(), postfix_stack.end());

        while (!postfix_stack.empty()) {
            std::string current_op = postfix_stack.back();
            postfix_stack.pop_back();
            if (!is_operator(current_op)) {
                result_stack.push_back(replace_all(current_op, "~", "-"));
            } else {
                std::string second_value = replace_all(pop_from(result_stack), "~", "-");
                std::string first_value = replace_all(pop_from(result_stack), "~", "-");
                result_stack.push_back(_calculate(first_value, second_value, current_op));
            }
        }

        // float(eval("*".join(result_stack)))
        if (result_stack.empty()) {
            throw std::runtime_error("eval(): empty expression");
        }
        double result = parse_number(result_stack.front());
        for (std::size_t i = 1; i < result_stack.size(); ++i) {
            result *= parse_number(result_stack[i]);
        }
        return result;
    }

    void prepare(const std::string& expression) {
        std::deque<std::string> op_stack;
        op_stack.push_back(",");
        std::vector<std::string> arr;
        arr.reserve(expression.size());
        for (char c : expression) arr.push_back(std::string(1, c));

        std::size_t current_index = 0;
        std::size_t count = 0;

        for (std::size_t i = 0; i < arr.size(); ++i) {
            const std::string& current_op = arr[i];
            if (is_operator(current_op)) {
                if (count > 0) {
                    postfix_stack.push_back(join_chars(arr, current_index, count));
                }
                std::string peek_op = back_of(op_stack);
                if (current_op == ")") {
                    while (back_of(op_stack) != "(") {
                        postfix_stack.push_back(pop_from(op_stack));
                    }
                    pop_from(op_stack);
                } else {
                    while (current_op != "(" && peek_op != "," &&
                           compare(current_op, peek_op)) {
                        postfix_stack.push_back(pop_from(op_stack));
                        peek_op = back_of(op_stack);
                    }
                    op_stack.push_back(current_op);
                }
                count = 0;
                current_index = i + 1;
            } else {
                count += 1;
            }
        }

        if (count > 1 || (count == 1 && !is_operator(arr[current_index]))) {
            postfix_stack.push_back(join_chars(arr, current_index, count));
        }

        while (back_of(op_stack) != ",") {
            postfix_stack.push_back(pop_from(op_stack));
        }
    }

    static bool is_operator(const std::string& c) {
        return c.size() == 1 && std::string("+-*/()%").find(c) != std::string::npos;
    }

    bool compare(std::string cur, std::string peek) const {
        if (cur == "%") cur = "/";
        if (peek == "%") peek = "/";
        return operat_priority[static_cast<unsigned char>(peek[0]) - 40] >=
               operat_priority[static_cast<unsigned char>(cur[0]) - 40];
    }

    static std::string _calculate(const std::string& first_value,
                                  const std::string& second_value,
                                  const std::string& current_op) {
        double first = parse_number(first_value);
        double second = parse_number(second_value);
        double result;
        if (current_op == "+") {
            result = first + second;
        } else if (current_op == "-") {
            result = first - second;
        } else if (current_op == "*") {
            result = first * second;
        } else if (current_op == "/") {
            if (second == 0.0) {
                throw std::runtime_error("decimal.DivisionByZero");
            }
            result = first / second;
        } else if (current_op == "%") {
            if (second == 0.0) {
                throw std::runtime_error("decimal.InvalidOperation");
            }
            // Decimal's % takes the sign of the dividend, same as fmod
            result = std::fmod(first, second);
        } else {
            throw std::invalid_argument("Unexpected operator: " + current_op);
        }
        return format_number(result);
    }

    static std::string transform(const std::string& expression) {
        std::string expr = std::regex_replace(expression, std::regex("\\s+"), "");
        expr = std::regex_replace(expr, std::regex("=$"), "");
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

        if (arr.at(0) == '~' && (arr.size() > 1 && arr[1] == '(')) {
            arr[0] = '-';
            return "0" + std::string(arr.begin(), arr.end());
        }
        return std::string(arr.begin(), arr.end());
    }

private:
    std::deque<std::string> postfix_stack;
    std::vector<int> operat_priority;

    static std::string replace_all(std::string s, const std::string& from,
                                   const std::string& to) {
        if (from.empty()) return s;
        std::size_t pos = 0;
        while ((pos = s.find(from, pos)) != std::string::npos) {
            s.replace(pos, from.size(), to);
            pos += to.size();
        }
        return s;
    }

    static std::string join_chars(const std::vector<std::string>& arr,
                                  std::size_t start, std::size_t count) {
        std::string out;
        for (std::size_t k = start; k < start + count && k < arr.size(); ++k) {
            out += arr[k];
        }
        return out;
    }

    static std::string pop_from(std::deque<std::string>& d) {
        if (d.empty()) throw std::out_of_range("pop from an empty deque");
        std::string v = d.back();
        d.pop_back();
        return v;
    }

    static const std::string& back_of(std::deque<std::string>& d) {
        if (d.empty()) throw std::out_of_range("deque index out of range");
        return d.back();
    }

    static double parse_number(const std::string& s) {
        const char* begin = s.c_str();
        char* end = nullptr;
        double v = std::strtod(begin, &end);
        if (end == begin) {
            throw std::invalid_argument("Invalid decimal literal: " + s);
        }
        return v;
    }

    static std::string format_number(double v) {
        char buf[64];
        std::snprintf(buf, sizeof(buf), "%.17g", v);
        return std::string(buf);
    }
};