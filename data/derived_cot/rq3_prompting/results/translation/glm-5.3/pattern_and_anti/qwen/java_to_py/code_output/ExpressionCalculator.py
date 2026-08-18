import math


def _ieee_div(a, b):
    # Java double division: 1.0/0.0 -> Infinity, 0.0/0.0 -> NaN (no exception)
    if b == 0.0:
        if math.isnan(a) or a == 0.0:
            return float('nan')
        return math.copysign(float('inf'), a) * math.copysign(1.0, b)
    return a / b


def _ieee_mod(a, b):
    # Java double remainder: sign of dividend (C fmod semantics), x % 0.0 -> NaN
    if math.isnan(a) or math.isnan(b) or math.isinf(a) or b == 0.0:
        return float('nan')
    return math.fmod(a, b)


class ExpressionCalculator:
    def __init__(self):
        self.postfixStack = []

    def calculate(self, expression):
        transformedExpression = self.transform(expression)
        self.prepare(transformedExpression)
        return self._evaluatePostfix()

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
                while (operatorStack and self.isOperator(operatorStack[-1])
                       and not self.compare(operatorStack[-1], ch)):
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

    def _evaluatePostfix(self):
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
            return _ieee_div(a, b)
        elif operator == '%':
            return _ieee_mod(a, b)
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