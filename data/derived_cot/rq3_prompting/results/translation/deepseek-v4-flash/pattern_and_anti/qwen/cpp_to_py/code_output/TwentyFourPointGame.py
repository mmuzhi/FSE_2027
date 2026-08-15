import random
import math


class TwentyFourPointGame:
    def __init__(self):
        self.nums = []
        random.seed()

    def generate_cards(self):
        for _ in range(4):
            self.nums.append(random.randint(1, 9))

    def get_my_cards(self):
        self.nums.clear()
        self.generate_cards()
        return self.nums.copy()

    def answer(self, expression):
        if expression == "pass":
            return self.get_my_cards()

        statistic = {}
        for c in expression:
            if '0' <= c <= '9' and (ord(c) - ord('0')) in self.nums:
                statistic[c] = statistic.get(c, 0) + 1

        nums_used = statistic.copy()

        for num in self.nums:
            key = chr(ord('0') + num)
            if key in nums_used and nums_used[key] > 0:
                nums_used[key] -= 1
            else:
                return []

        if all(v == 0 for v in nums_used.values()):
            if self.evaluate_expression(expression):
                return [1]
            else:
                return []
        else:
            return []

    def evaluate_expression(self, expression):
        try:
            if not expression:
                return False
            if not ('0' <= expression[0] <= '9') and expression[0] != '(':
                return False
            kkk = len(expression) - 1
            if not ('0' <= expression[kkk] <= '9') and expression[kkk] != ')':
                return False

            calculator = Calculator()
            ans = calculator.calculate(expression)
            return ans == 24.0
        except Exception:
            return False

    def set_nums(self, now):
        self.nums = list(now)


class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': self._div,
            '^': self._pow,
        }

    @staticmethod
    def _div(x, y):
        if y == 0.0:
            if x == 0.0:
                return float('nan')
            if x > 0:
                return float('inf')
            if x < 0:
                return float('-inf')
            return float('nan')
        return x / y

    @staticmethod
    def _pow(x, y):
        try:
            if math.isnan(x) or math.isnan(y):
                return float('nan')
            if x == 0.0:
                if y == 0.0:
                    return 1.0
                if y < 0:
                    return float('inf')
                return 0.0
            if x < 0 and y != int(y):
                return float('nan')
            return x ** y
        except Exception:
            return float('nan')

    @staticmethod
    def _parse_number(s):
        i = 0
        n = len(s)

        while i < n and '0' <= s[i] <= '9':
            i += 1

        if i < n and s[i] == '.':
            i += 1
            while i < n and '0' <= s[i] <= '9':
                i += 1

        if i == 0:
            raise ValueError("invalid number")
        return float(s[:i])

    def calculate(self, expression):
        if not expression:
            return 0.0

        operand_stack = []
        operator_stack = []
        num_buffer = []

        for ch in expression:
            if ('0' <= ch <= '9') or ch == '.':
                num_buffer.append(ch)
            else:
                if num_buffer:
                    operand_stack.append(self._parse_number(''.join(num_buffer)))
                    num_buffer.clear()

                if ch in '+-*/^':
                    while (operator_stack and operator_stack[-1] != '(' and
                           self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()

        if num_buffer:
            operand_stack.append(self._parse_number(''.join(num_buffer)))

        while operator_stack:
            self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0

    def precedence(self, op):
        if op in '+-':
            return 1
        if op in '*/':
            return 2
        if op == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        op = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = self.operators[op](operand1, operand2)
        operand_stack.append(result)