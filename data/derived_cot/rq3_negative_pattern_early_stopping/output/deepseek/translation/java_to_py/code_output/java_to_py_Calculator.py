class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y
        }

    def calculate(self, expression: str):
        operand_stack = []
        operator_stack = []
        num_buffer = []

        for i, ch in enumerate(expression):
            if ch.isdigit() or ch == '.':
                num_buffer.append(ch)
            else:
                if num_buffer:
                    operand_stack.append(float(''.join(num_buffer)))
                    num_buffer = []

                if ch in self.operators:
                    while (operator_stack and
                           operator_stack[-1] != '(' and
                           self._precedence(operator_stack[-1]) >= self._precedence(ch)):
                        self._apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        self._apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()

        if num_buffer:
            operand_stack.append(float(''.join(num_buffer)))

        while operator_stack:
            self._apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else None

    def _precedence(self, op: str) -> int:
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        if op == '^':
            return 3
        return 0

    def _apply_operator(self, operand_stack: list, operator_stack: list):
        op = operator_stack.pop()
        b = operand_stack.pop()
        a = operand_stack.pop()
        operand_stack.append(self.operators[op](a, b))

if __name__ == '__main__':
    calc = Calculator()
    print(calc.calculate("1+2-3"))