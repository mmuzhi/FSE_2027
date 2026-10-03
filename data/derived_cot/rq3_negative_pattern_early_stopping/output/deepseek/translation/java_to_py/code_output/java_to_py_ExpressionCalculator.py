class ExpressionCalculator:
    def __init__(self):
        self.postfixStack = []

    def calculate(self, expression):
        transformed_expression = self.transform(expression)
        self.prepare(transformed_expression)
        return self.evaluate_postfix()

    def prepare(self, expression):
        self.postfixStack.clear()
        operator_stack = []
        length = len(expression)
        i = 0
        while i < length:
            ch = expression[i]
            if ch.isdigit() or ch == '.':
                num = []
                while i < length and (expression[i].isdigit() or expression[i] == '.'):
                    num.append(expression[i])
                    i += 1
                i -= 1
                self.postfixStack.append(''.join(num))
            elif ch == '(':
                operator_stack.append(ch)
            elif ch == ')':
                while operator_stack and operator_stack[-1] != '(':
                    self.postfixStack.append(str(operator_stack.pop()))
                operator_stack.pop()
            elif self.is_operator(ch):
                while operator_stack and self.is_operator(operator_stack[-1]) and not self.compare(operator_stack[-1], ch):
                    self.postfixStack.append(str(operator_stack.pop()))
                operator_stack.append(ch)
            i += 1
        while operator_stack:
            self.postfixStack.append(str(operator_stack.pop()))

    def is_operator(self, ch):
        return ch in ('+', '-', '*', '/', '%')

    def compare(self, op1, op2):
        cur_op = '/' if op1 == '%' else op1
        peek_op = '/' if op2 == '%' else op2
        operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]
        return operat_priority[ord(peek_op) - 40] >= operat_priority[ord(cur_op) - 40]

    def evaluate_postfix(self):
        stack = []
        import math
        for token in self.postfixStack:
            if len(token) == 1 and self.is_operator(token[0]):
                b = stack.pop()
                a = stack.pop()
                stack.append(self._calculate(a, b, token[0]))
            else:
                stack.append(float(token))
        return stack.pop()

    def _calculate(self, a, b, operator):
        import math
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            return a / b
        elif operator == '%':
            return math.fmod(a, b)
        else:
            raise ValueError("Unsupported operator: " + operator)

    def transform(self, expression):
        expression = expression.replace(' ', '')
        expression = expression.replace('-', '~')
        chars = list(expression)
        if len(chars) > 1 and chars[0] == '~' and chars[1] == '(':
            chars[0] = '-'
            expression = ''.join(chars)
            return '0' + expression
        else:
            return expression