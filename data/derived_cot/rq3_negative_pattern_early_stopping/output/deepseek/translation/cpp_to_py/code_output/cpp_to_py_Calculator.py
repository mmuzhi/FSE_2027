import math

class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: math.pow(x, y),
        }

    def calculate(self, expression: str) -> float:
        if not expression:
            return 0.0

        operand_stack = []
        operator_stack = []
        num_buffer = ""

        for ch in expression:
            if ch.isdigit() or ch == '.':
                num_buffer += ch
            else:
                if num_buffer:
                    operand_stack.append(float(num_buffer))
                    num_buffer = ""

                if ch in "+-*/^":
                    while (operator_stack and operator_stack[-1] != '(' and
                           self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()  # remove '('

        if num_buffer:
            operand_stack.append(float(num_buffer))

        while operator_stack:
            self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0

    def precedence(self, op: str) -> int:
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        if op == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack: list, operator_stack: list) -> None:
        op = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = self.operators[op](operand1, operand2)
        operand_stack.append(result)