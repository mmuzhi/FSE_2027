#include <algorithm>
#include <stdexcept>
#include <string>
#include <vector>

/*
# This is a class that checks for bracket matching
*/
class BalancedBrackets {
public:
    /*
    Initializes the class with an expression.
    :param expr: The expression to check for balanced brackets, str.
    */
    explicit BalancedBrackets(std::string expr)
        : left_brackets{'(', '{', '['},
          right_brackets{')', '}', ']'},
          expr(std::move(expr)) {}

    /*
    Clears the expression of all characters that are not brackets.
    */
    void clear_expr() {
        std::string filtered;
        for (char c : expr) {
            if (is_left_bracket(c) || is_right_bracket(c)) {
                filtered += c;
            }
        }
        expr = filtered;
    }

    /*
    Checks if the expression has balanced brackets.
    :return: true if the expression has balanced brackets, false otherwise.
    */
    bool check_balanced_brackets() {
        clear_expr();
        for (char Brkt : expr) {
            if (is_left_bracket(Brkt)) {
                stack.push_back(Brkt);
            } else {
                // Python's list.pop() raises IndexError on an empty list.
                if (stack.empty()) {
                    throw std::out_of_range("pop from empty list");
                }
                char Current_Brkt = stack.back();
                stack.pop_back();
                if (Current_Brkt == '(') {
                    if (Brkt != ')') {
                        return false;
                    }
                }
                if (Current_Brkt == '{') {
                    if (Brkt != '}') {
                        return false;
                    }
                }
                if (Current_Brkt == '[') {
                    if (Brkt != ']') {
                        return false;
                    }
                }
            }
        }
        if (!stack.empty()) {
            return false;
        }
        return true;
    }

private:
    std::vector<char> stack;
    std::vector<char> left_brackets;
    std::vector<char> right_brackets;
    std::string expr;

    bool is_left_bracket(char c) const {
        return std::find(left_brackets.begin(), left_brackets.end(), c) != left_brackets.end();
    }

    bool is_right_bracket(char c) const {
        return std::find(right_brackets.begin(), right_brackets.end(), c) != right_brackets.end();
    }
};