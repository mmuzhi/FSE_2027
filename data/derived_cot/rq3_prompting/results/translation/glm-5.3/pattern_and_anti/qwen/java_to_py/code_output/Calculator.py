import math


class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': self._div,
            '^': lambda x, y: math.pow(x, y),
        }

    @staticmethod
    def _div(x, y):
        # Java double division by zero yields Infinity/NaN rather than raising
        try:
            return x / y
        except ZeroDivisionError:
            if x == 0.0:
                return math.nan
            return math.inf if x > 0 else -math.inf

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
                    while (operator_stack
                           and operator_stack[-1] != '('
                           and self.precedence(operator_stack[-1]) >= self.precedence(ch)):
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