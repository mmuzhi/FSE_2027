import math
import re


class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': Calculator._div,
            '^': Calculator._pow,
        }

    @staticmethod
    def _div(x, y):
        # IEEE-754 double semantics like C++ (no exception on divide by zero)
        if y != 0.0:
            return x / y
        if x == 0.0:
            return float('nan')
        return math.copysign(float('inf'), x) * math.copysign(1.0, y)

    @staticmethod
    def _pow(x, y):
        # std::pow semantics: yield inf/nan instead of raising
        try:
            return math.pow(x, y)
        except OverflowError:
            if x < 0 and y.is_integer() and int(y) % 2:
                return float('-inf')
            return float('inf')
        except ValueError:
            if x == 0.0 and y < 0:
                return float('inf')
            return float('nan')

    @staticmethod
    def _stod(s):
        # Mimic std::stod on buffers of digits/dots: longest valid prefix,
        # ValueError (≈ std::invalid_argument) when no conversion exists.
        m = re.match(r'\d+\.?\d*|\.\d+', s)
        if m is None:
            raise ValueError(f'stod: no conversion: "{s}"')
        return float(m.group())

    def calculate(self, expression: str) -> float:
        if not expression:
            return 0.0

        operand_stack = []
        operator_stack = []
        num_buffer = ''

        for ch in expression:
            if ch in '0123456789' or ch == '.':
                num_buffer += ch
            else:
                if num_buffer:
                    operand_stack.append(self._stod(num_buffer))
                    num_buffer = ''

                if ch in '+-*/^':
                    while (operator_stack and operator_stack[-1] != '('
                           and self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        operand_stack, operator_stack = self.apply_operator(
                            operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        operand_stack, operator_stack = self.apply_operator(
                            operand_stack, operator_stack)
                    operator_stack.pop()

        if num_buffer:
            operand_stack.append(self._stod(num_buffer))

        while operator_stack:
            operand_stack, operator_stack = self.apply_operator(
                operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0

    @staticmethod
    def precedence(op):
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

        return operand_stack, operator_stack