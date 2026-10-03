from collections import deque
import re

class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = deque()
    
    def calculate(self, expression):
        transformed = self.transform(expression)
        self.prepare(transformed)
        return self.evaluate_postfix()
    
    def transform(self, expression):
        expression = re.sub(r'\s+', '', expression)
        expression = expression.replace('-', '~')
        if len(expression) > 0 and expression[0] == '~' and expression[1] == '(':
            expression = '0' + expression
            expression = list(expression)
            expression[0] = '-'
            return ''.join(expression)
        return expression

    def prepare(self, expression):
        self.postfix_stack.clear()
        operator_stack = deque()
        i = 0
        while i < len(expression):
            char = expression[i]
            if char.isdigit() or char == '.':
                num_str = ''
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num_str += expression[i]
                    i += 1
                self.postfix_stack.append(num_str)
            elif char == '(':
                operator_stack.append(char)
            elif char == ')':
                while operator_stack and operator_stack[-1] != '(':
                    self.postfix_stack.append(operator_stack.pop())
                operator_stack.pop()
            elif self.is_operator(char):
                while operator_stack and self.is_operator(operator_stack[-1]) and not self.compare(operator_stack[-1], char):
                    self.postfix_stack.append(operator_stack.pop())
                operator_stack.append(char)
            i += 1
        while operator_stack:
            self.postfix_stack.append(operator_stack.pop())
    
    def is_operator(self, char):
        return char in '+-*/%'
    
    def compare(self, op1, op2):
        op1_mapped = '/' if op1 == '%' else op1
        op2_mapped = '/' if op2 == '%' else op2
        precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2,
            '%': 2
        }
        return precedence[op1_mapped] >= precedence[op2_mapped]
    
    def evaluate_postfix(self):
        stack = deque()
        for token in self.postfix_stack:
            if self.is_operator(token[0]):
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
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        elif operator == '%':
            return a % b
        else:
            raise ValueError(f"Unsupported operator: {operator}")