class Calculator:
    def __init__(self):
        self.operators = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide,
            '^': self.power
        }

    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        return x / y

    def power(self, x, y):
        return pow(x, y)

    def calculate(self, expression):
        if not expression:
            raise ValueError("Input expression is empty")
        
        operand_stack = []
        operator_stack = []
        num_buffer = []

        for ch in expression:
            if ch.isdigit() or ch == '.':
                num_buffer.append(ch)
            else:
                self._handle_number(num_buffer, operand_stack)
                
                if ch in self.operators:
                    self._apply_operators(operand_stack, operator_stack, ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    self._apply_operators(operand_stack, operator_stack, None)
                    if operator_stack and operator_stack[-1] == '(':
                        operator_stack.pop()
        
        self._handle_number(num_buffer, operand_stack)
        
        while operator_stack:
            self._apply_operators(operand_stack, operator_stack, None)
        
        return operand_stack[-1] if operand_stack else None

    def _handle_number(self, num_buffer, operand_stack):
        if num_buffer:
            try:
                num = float(''.join(num_buffer))
                operand_stack.append(num)
            except ValueError:
                raise ValueError("Invalid number format") from None
            num_buffer.clear()

    def _apply_operators(self, operand_stack, operator_stack, next_operator):
        while operator_stack:
            op = operator_stack[-1]
            if op == '(':
                break
            if next_operator is not None and self._precedence(op) > self._precedence(next_operator):
                break
            operator_stack.pop()
            if op == '^':
                operand_stack.append(self.operators[op](operand_stack.pop(), operand_stack.pop()))
            else:
                operand_stack.append(self.operators[op](operand_stack.pop(), operand_stack.pop()))

    def _precedence(self, operator):
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        elif operator == '^':
            return 3
        return 0

if __name__ == "__main__":
    calculator = Calculator()
    print(calculator.calculate("1+2-3"))  # Example usage