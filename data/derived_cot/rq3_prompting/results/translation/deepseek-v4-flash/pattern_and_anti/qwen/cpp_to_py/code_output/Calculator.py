import math

def _parse_number(s):
    try:
        val = float(s)
    except ValueError:
        raise ValueError("invalid number")
    if math.isinf(val):
        raise OverflowError("value out of range")
    return val

def _div(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        if x == 0.0 or math.isnan(x):
            return float('nan')
        sign = math.copysign(1.0, x) * math.copysign(1.0, y)
        return math.inf * sign

def _pow(x, y):
    try:
        return math.pow(x, y)
    except ValueError:
        if x == 0.0:
            if math.copysign(1.0, x) < 0 and math.isfinite(y) and y == int(y) and int(y) % 2 != 0:
                return -math.inf
            return math.inf
        return float('nan')
    except OverflowError:
        if x < 0 and math.isfinite(y) and y == int(y) and int(y) % 2 != 0:
            return -math.inf
        return math.inf

class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': _div,
            '^': _pow,
        }

    def calculate(self, expression):
        if expression == "":
            return 0.0

        operand_stack = []
        operator_stack = []
        num_buffer = ""

        for ch in expression:
            if ('0' <= ch <= '9') or ch == '.':
                num_buffer += ch
            else:
                if num_buffer:
                    operand_stack.append(_parse_number(num_buffer))
                    num_buffer = ""

                if ch in ('+', '-', '*', '/', '^'):
                    while (operator_stack and operator_stack[-1] != '(' and
                           self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()

        if num_buffer:
            operand_stack.append(_parse_number(num_buffer))

        while operator_stack:
            operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0

    def precedence(self, op):
        if op in ('+', '-'):
            return 1
        elif op in ('*', '/'):
            return 2
        elif op == '^':
            return 3
        else:
            return 0

    def apply_operator(self, operand_stack, operator_stack):
        operand_stack = operand_stack[:]
        operator_stack = operator_stack[:]
        op = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = self.operators[op](operand1, operand2)
        operand_stack.append(result)
        return operand_stack, operator_stack