import math

class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: math.pow(x, y)
        }

    def calculate(self, expression):
        operand_stack = []
        operator_stack = []
        num_buffer = []

        for ch in expression:
            if ch.isdigit() or ch == '.':
                num_buffer.append(ch)
            else:
                if len(num_buffer) > 0:
                    operand_stack.append(float(''.join(num_buffer)))
                    num_buffer.clear()

                if ch in self.operators:
                    while (len(operator_stack) > 0 and
                           operator_stack[-1] != '(' and
                           self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while len(operator_stack) > 0 and operator_stack[-1] != '(':
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()

        if len(num_buffer) > 0:
            operand_stack.append(float(''.join(num_buffer)))

        while len(operator_stack) > 0:
            self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if len(operand_stack) > 0 else None

    def precedence(self, operator):
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        elif operator == '^':
            return 3
        else:
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