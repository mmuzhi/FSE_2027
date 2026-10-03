#include <vector>
#include <string>
#include <random>
#include <cctype>
#include <stdexcept>

class TwentyFourPointGame {
private:
    std::vector<int> nums;
    int pos;
    int ch;
    std::string expr;

    std::vector<int> getMyCards() {
        std::vector<int> cards;
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> dis(1, 9);
        for (int i = 0; i < 4; ++i) {
            cards.push_back(dis(gen));
        }
        return cards;
    }

    void nextChar() {
        ch = (++pos < (int)expr.length()) ? expr[pos] : -1;
    }

    bool eat(int charToEat) {
        while (ch == ' ') nextChar();
        if (ch == charToEat) {
            nextChar();
            return true;
        }
        return false;
    }

    double parse() {
        nextChar();
        double x = parseExpression();
        if (pos < (int)expr.length()) throw std::runtime_error("Unexpected");
        return x;
    }

    double parseExpression() {
        double x = parseTerm();
        for (;;) {
            if (eat('+')) x += parseTerm();
            else if (eat('-')) x -= parseTerm();
            else return x;
        }
    }

    double parseTerm() {
        double x = parseFactor();
        for (;;) {
            if (eat('*')) x *= parseFactor();
            else if (eat('/')) x /= parseFactor();
            else return x;
        }
    }

    double parseFactor() {
        if (eat('+')) return parseFactor();
        if (eat('-')) return -parseFactor();

        double x;
        int startPos = this->pos;
        if (eat('(')) {
            x = parseExpression();
            eat(')');
        } else if ((ch >= '0' && ch <= '9') || ch == '.') {
            while ((ch >= '0' && ch <= '9') || ch == '.') nextChar();
            x = std::stod(expr.substr(startPos, this->pos - startPos));
        } else {
            throw std::runtime_error("Unexpected");
        }

        return x;
    }

    bool evaluateExpression(const std::string& expression) {
        try {
            expr = expression;
            pos = -1;
            ch = -1;
            return parse() == 24;
        } catch (std::exception& e) {
            return false;
        }
    }

public:
    TwentyFourPointGame() {
        this->nums = getMyCards();
    }

    bool answer(const std::string& expression) {
        if (expression == "pass") {
            this->nums = getMyCards();
            return false;
        }

        int counts[10] = {0};
        for (char c : expression) {
            if (std::isdigit(c)) {
                counts[c - '0']++;
            }
        }

        for (int num : nums) {
            if (counts[num] > 0) {
                counts[num]--;
            } else {
                return false;
            }
        }

        for (int count : counts) {
            if (count != 0) {
                return false;
            }
        }

        return evaluateExpression(expression);
    }

    std::vector<int> getNums() {
        return nums;
    }
};