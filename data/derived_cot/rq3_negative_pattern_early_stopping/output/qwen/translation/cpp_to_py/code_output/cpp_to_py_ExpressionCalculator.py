import re

class ExpressionCalculator:
    OPERATORS = {'+', '-', '*', '/', '(', ')', '%'}
    priority = {
        '(': 0,
        ')': 3,
        '+': 2,
        '-': 1,
        '*': 2,
        '/': 2,
        '%': 2
    }

    def __init__(self):
        self.postfix_stack = []
        self.op_stack = [',']  # Initial sentinel

    @staticmethod
    def is_operator(c):
        return c in ExpressionCalculator.OPERATORS

    def compare(self, cur, peek):
        if cur == '%':
            cur_op = '/'
        else:
            cur_op = cur

        if peek == '%':
            peek_op = '/'
        else:
            peek_op = peek

        if cur_op in self.priority and peek_op in self.priority:
            return self.priority[peek_op] >= self.priority[cur_op]
        return False

    @staticmethod
    def _calculate(first_value, second_value, current_op):
        try:
            f = float(first_value)
            s = float(second_value)
        except ValueError:
            raise ValueError("Invalid number format")

        if current_op == "+":
            return f + s
        elif current_op == "-":
            return f - s
        elif current_op == "*":
            return f * s
        elif current_op == "/":
            return f / s
        elif current_op == "%":
            return f % s

        raise ValueError(f"Unexpected operator: {current_op}")

    @staticmethod
    def transform(expression):
        expr = re.sub(r'\s+', '', expression)
        expr = re.sub(r'=$', '', expr)

        new_expr = []
        for i, char in enumerate(expr):
            if char == '-':
                if i == 0:
                    new_expr.append('~')
                else:
                    prev_char = expr[i-1]
                    if prev_char in '+-*/()Ee':
                        new_expr.append('~')
                    else:
                        new_expr.append('-')
            else:
                new_expr.append(char)

        expr = ''.join(new_expr)

        if expr.startswith('~') and len(expr) > 1 and expr[1] == '(':
            expr = '0' + expr.replace('~', '-', 1)

        return expr.replace('~', '-')

    def prepare(self, expression):
        self.postfix_stack = []
        self.op_stack = [',']  # Reset operator stack

        n = len(expression)
        i = 0
        current_index = 0
        count = 0

        while i < n:
            c = expression[i]
            current_op = c

            if self.is_operator(current_op):
                if count > 0:
                    num_str = expression[current_index:current_index+count]
                    if count > 1 or (count == 1 and not self.is_operator(num_str)):
                        self.postfix_stack.append(num_str)
                    count = 0

                if current_op == ')':
                    while self.op_stack[-1] != '(':
                        if self.op_stack[-1] == ',':
                            break
                        op = self.op_stack.pop()
                        self.postfix_stack.append(op)
                    if self.op_stack[-1] == '(':
                        self.op_stack.pop()
                else:
                    while (current_op != '(' and 
                           self.op_stack[-1] != ',' and 
                           self.compare(current_op, self.op_stack[-1])):
                        op = self.op_stack.pop()
                        self.postfix_stack.append(op)
                    self.op_stack.append(current_op)

                current_index = i + 1
                count = 0
                i += 1
            else:
                count += 1
                i += 1

        if count > 0:
            num_str = expression[current_index:current_index+count]
            if count > 1 or (count == 1 and not self.is_operator(num_str)):
                self.postfix_stack.append(num_str)

        while self.op_stack[-1] != ',':
            op = self.op_stack.pop()
            self.postfix_stack.append(op)

    def calculate(self, expression):
        transformed_expr = self.transform(expression)
        self.prepare(transformed_expr)

        reversed_postfix_stack = list(reversed(self.postfix_stack))
        result_stack = []

        while reversed_postfix_stack:
            token = reversed_postfix_stack.pop()
            if not self.is_operator(token):
                token = token.replace('~', '-')
                result_stack.append(token)
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()
                first_value = first_value.replace('~', '-')
                second_value = second_value.replace('~', '-')
                try:
                    result = self._calculate(first_value, second_value, token)
                    result_stack.append(str(result))
                except Exception as e:
                    raise ValueError(f"Calculation error: {str(e)}")

        result_str = "*".join(result_stack)
        if result_str.endswith('*'):
            result_str = result_str[:-1]
        try:
            return float(result_str)
        except Exception as e:
            raise ValueError(f"Invalid result string: {result_str}")