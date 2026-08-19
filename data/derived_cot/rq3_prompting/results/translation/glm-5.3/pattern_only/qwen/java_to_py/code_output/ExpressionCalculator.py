import math


class ExpressionCalculator:

    def __init__(self):
        self.postfixStack = []

    def calculate(self, expression):
        transformedExpression = self.transform(expression)
        self.prepare(transformedExpression)
        return self.evaluatePostfix()

    def prepare(self, expression):
        self.postfixStack.clear()
        operatorStack = []
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
                operatorStack.append(ch)
            elif ch == ')':
                while operatorStack and operatorStack[-1] != '(':
                    self.postfixStack.append(operatorStack.pop())
                operatorStack.pop()
            elif self.isOperator(ch):
                while operatorStack and self.isOperator(operatorStack[-1]) and not self.compare(operatorStack[-1], ch):
                    self.postfixStack.append(operatorStack.pop())
                operatorStack.append(ch)
            i += 1
        while operatorStack:
            self.postfixStack.append(operatorStack.pop())

    def isOperator(self, ch):
        return ch == '+' or ch == '-' or ch == '*' or ch == '/' or ch == '%'

    def compare(self, op1, op2):
        cur_op = '/' if op1 == '%' else op1
        peek_op = '/' if op2 == '%' else op2
        operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]
        return operat_priority[ord(peek_op) - 40] >= operat_priority[ord(cur_op) - 40]

    def evaluatePostfix(self):
        stack = []
        for token in self.postfixStack:
            if self.isOperator(token[0]):
                b = stack.pop()
                a = stack.pop()
                stack.append(self._calculate(a, b, token[0]))
            else:
                stack.append(float(token))
        return stack.pop()

    def _calculate(self, a, b, operator):
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0.0:
                # Java double division by zero yields IEEE inf/nan, not an exception
                if a == 0.0 or math.isnan(a):
                    return float('nan')
                sign = math.copysign(1.0, a) * math.copysign(1.0, b)
                return math.copysign(float('inf'), sign)
            return a / b
        elif operator == '%':
            # Java double % is C-style fmod (sign of dividend), not Python's floor-based %
            if b == 0.0 or math.isinf(a) or math.isnan(a) or math.isnan(b):
                return float('nan')
            return math.fmod(a, b)
        else:
            raise ValueError("Unsupported operator: " + operator)

    def transform(self, expression):
        expression = expression.replace(" ", "")
        expression = expression.replace("-", "~")
        if expression[0] == '~' and len(expression) > 1 and expression[1] == '(':
            expression = '-' + expression[1:]
            return "0" + expression
        else:
            return expression