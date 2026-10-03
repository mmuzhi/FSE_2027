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
        if expression == "":
            return 0.0

        operand_stack = []
        operator_stack = []
        num_buffer = ""

        for ch in expression:
            if ch in '0123456789.':
                num_buffer += ch
            else:
                if num_buffer != "":
                    operand_stack.append(float(num_buffer))
                    num_buffer = ""
                if ch in '+-*/^':
                    while operator_stack and operator_stack[-1] != '(' and self.precedence(operator_stack[-1]) >= self.precedence(ch):
                        self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        self.apply_operator(operand_stack, operator_stack)
                    if operator_stack and operator_stack[-1] == '(':
                        operator_stack.pop()

        if num_buffer != "":
            operand_stack.append(float(num_buffer))

        while operator_stack:
            self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0

    def precedence(self, op):
        if op in '+-':
            return 1
        elif op in '*/':
            return 2
        elif op == '^':
            return 3
        else:
            return 0

    def apply_operator(self, operand_stack, operator_stack):
        if not operand_stack or not operator_stack or operator_stack[-1] == '(':
            raise Exception("Invalid expression")

        op = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()

        result = self.operators[op](operand1, operand2)
        operand_stack.append(result)