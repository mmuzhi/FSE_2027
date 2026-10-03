#include <iostream>
#include <vector>
#include <cctype>
#include <string>
#include <stack>
#include <algorithm>
#include <unordered_map>
#include <cassert>

// Function to tokenize the expression into tokens (each digit is a token, and operators and parentheses are tokens)
std::vector<std::string> tokenize(const std::string& expression) {
    std::vector<std::string> tokens;
    std::string current;
    for (char c : expression) {
        if (std::isdigit(c)) {
            // Each digit is a separate token
            if (!current.empty()) {
                tokens.push_back(current);
                current.clear();
            }
            current.push_back(c);
        } else if (c == '+' || c == '-' || c == '*' || c == '/' || c == '(' || c == ')') {
            if (!current.empty()) {
                tokens.push_back(current);
                current.clear();
            }
            tokens.push_back(std::string(1, c));
        }
        // Ignore spaces? The Python code does not mention spaces, but `eval` ignores them.
        // We'll ignore spaces.
        else if (c == ' ') {
            if (!current.empty()) {
                tokens.push_back(current);
                current.clear();
            }
        }
    }
    if (!current.empty()) {
        tokens.push_back(current);
    }
    return tokens;
}

// Function to check if a token is a number (single-digit)
bool isNumber(const std::string& token) {
    return !token.empty() && std::isdigit(token[0]);
}

// Function to check if a token is an operator
bool isOperator(const std::string& token) {
    return token == "+" || token == "-" || token == "*" || token == "/";
}

// Function to check if a token is an opening parenthesis
bool isLeftParen(const std::string& token) {
    return token == "(";
}

// Function to check if a token is a closing parenthesis
bool isRightParen(const std::string& token) {
    return token == ")";
}

// Function to evaluate the expression given the tokens
double evaluateExpression(const std::vector<std::string>& tokens) {
    // Convert tokens to RPN using the shunting yard algorithm
    std::vector<std::string> output;
    std::stack<std::string> operators;

    // Precedence of operators
    std::unordered_map<std::string, int> precedence = {
        {"+", 1},
        {"-", 1},
        {"*", 2},
        {"/", 2}
    };

    for (const std::string& token : tokens) {
        if (isNumber(token)) {
            output.push_back(token);
        } else if (isOperator(token)) {
            while (!operators.empty() && isOperator(operators.top()) && 
                   precedence[operators.top()] >= precedence[token]) {
                output.push_back(operators.top());
                operators.pop();
            }
            operators.push(token);
        } else if (isLeftParen(token)) {
            operators.push(token);
        } else if (isRightParen(token)) {
            while (!operators.empty() && isOperator(operators.top()) && operators.top() != "(") {
                output.push_back(operators.top());
                operators.pop();
            }
            if (!operators.empty() && operators.top() == "(") {
                operators.pop();
            }
            // If there's a mismatched parenthesis, return an error (but the problem doesn't specify)
            // We'll assume well-formed expression.
        }
    }

    while (!operators.empty()) {
        output.push_back(operators.top());
        operators.pop();
    }

    // Now evaluate the RPN
    std::stack<double> values;
    for (const std::string& token : output) {
        if (isNumber(token)) {
            values.push(std::stoi(token));
        } else if (isOperator(token)) {
            if (values.size() < 2) {
                // Error: not enough operands
                return 0;
            }
            double b = values.top(); values.pop();
            double a = values.top(); values.pop();
            if (token == "+") {
                values.push(a + b);
            } else if (token == "-") {
                values.push(a - b);
            } else if (token == "*") {
                values.push(a * b);
            } else if (token == "/") {
                if (b == 0) {
                    // Division by zero
                    return 0;
                }
                values.push(a / b);
            }
        }
    }

    if (values.size() != 1) {
        // Error: wrong number of operands
        return 0;
    }

    return values.top();
}

class TwentyFourPointGame {
private:
    std::vector<int> nums;

    // Helper function to generate four random numbers between 1 and 9
    void _generate_cards() {
        for (int i = 0; i < 4; i++) {
            nums.push_back(random() % 9 + 1);
        }
        assert(nums.size() == 4);
    }

public:
    TwentyFourPointGame() {
        nums.clear();
    }

    // Get the player's cards (resets the current cards and generates new ones)
    std::vector<int> get_my_cards() {
        nums.clear();
        _generate_cards();
        return nums;
    }

    // Check if the expression evaluates to 24 and uses the four cards exactly once
    bool answer(const std::string& expression) {
        if (expression == "pass") {
            return get_my_cards();
        }

        // Count the frequency of each digit in the expression
        std::unordered_map<char, int> statistic;
        for (char c : expression) {
            if (std::isdigit(c)) {
                int num = c - '0';
                if (std::find(nums.begin(), nums.end(), num) != nums.end()) {
                    statistic[c] = statistic.get(c, 0) + 1;
                }
            }
        }

        // Check that we used each card exactly once
        std::vector<int> nums_used;
        for (int num : nums) {
            char digit = '0' + num;
            if (statistic.find(digit) != statistic.end() && statistic[digit] > 0) {
                statistic[digit]--;
            } else {
                return false;
            }
        }

        // Check that all cards are used exactly once
        for (const auto& pair : statistic) {
            if (pair.second != 0) {
                return false;
            }
        }

        // Now, evaluate the expression
        try {
            std::vector<std::string> tokens = tokenize(expression);
            double result = evaluateExpression(tokens);
            return result == 24;
        } catch (...) {
            return false;
        }
    }
};

int main() {
    // Example usage
    TwentyFourPointGame game;
    game.get_my_cards();
    std::vector<int> cards = game.get_my_cards();
    std::cout << "Your cards: ";
    for (int card : cards) {
        std::cout << card << " ";
    }
    std::cout << std::endl;

    std::string expression = "4*3+6+6";
    bool result = game.answer(expression);
    std::cout << "Result: " << (result ? "True" : "False") << std::endl;

    return 0;
}