import math


def _java_pow(x, y):
    # Match Java Math.pow edge behavior instead of Python's `**`
    # (which returns a complex number for e.g. (-8) ** 0.5).
    try:
        return math.pow(x, y)
    except ValueError:
        return float('nan')
    except OverflowError:
        if x < 0 and y == int(y) and int(y) % 2 == 1:
            return -math.inf
        return math.inf


class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': _java_pow,
        }

    def calculate(self, expression):
        operand_stack = []
        operator_stack = []
        num_buffer = []

        for ch in expression:
            if ch.isdigit() or ch == '.':
                num_buffer.append(ch)
            else:
                if num_buffer:
                    operand_stack.append(float(''.join(num_buffer)))
                    num_buffer.clear()

                if ch in self.operators:
                    while (operator_stack and
                           operator_stack[-1] != '(' and
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
            operand_stack.append(float(''.join(num_buffer)))

        while operator_stack:
            self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else None

    def precedence(self, operator):
        if operator in ('+', '-'):
            return 1
        if operator in ('*', '/'):
            return 2
        if operator == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack, operator_stack):
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = self.operators[operator](operand1, operand2)
        operand_stack.append(result)


if __name__ == '__main__':
    calculator = Calculator()
    print(calculator.calculate("1+2-3"))