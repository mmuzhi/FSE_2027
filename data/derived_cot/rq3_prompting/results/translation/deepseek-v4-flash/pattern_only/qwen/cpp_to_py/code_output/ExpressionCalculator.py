import re
import math


def to_string_cpp(x):
    return format(x, '.6f')


def stod(s):
    i = 0
    n = len(s)
    while i < n and s[i].isspace():
        i += 1
    if i >= n:
        raise ValueError("stod: no conversion")

    start = i
    if s[i] in ('+', '-'):
        i += 1

    if s[i:i + 3].lower() == 'inf':
        i += 3
        if s[i:i + 5].lower() == 'inity':
            i += 5
        return float(s[start:i])

    if s[i:i + 3].lower() == 'nan':
        i += 3
        return float(s[start:i])

    seen_digit = False
    while i < n and s[i].isdigit():
        i += 1
        seen_digit = True

    if i < n and s[i] == '.':
        i += 1
        while i < n and s[i].isdigit():
            i += 1
            seen_digit = True

    if not seen_digit:
        raise ValueError("stod: no conversion")

    if i < n and s[i] in ('e', 'E'):
        j = i + 1
        if j < n and s[j] in ('+', '-'):
            j += 1
        if j < n and s[j].isdigit():
            i = j
            while i < n and s[i].isdigit():
                i += 1

    return float(s[start:i])


class ExpressionCalculator:
    def __init__(self):
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]
        self.postfix_stack = []

    @staticmethod
    def is_operator(c):
        return c in {'+', '-', '*', '/', '(', ')', '%'}

    def compare(self, cur, peek):
        cur_op = "/" if cur == "%" else cur
        peek_op = "/" if peek == "%" else peek
        return self.operat_priority[ord(peek_op[0]) - 40] >= self.operat_priority[ord(cur_op[0]) - 40]

    @staticmethod
    def _calculate(first_value, second_value, current_op):
        f = stod(first_value)
        s = stod(second_value)

        if current_op == "+":
            return f + s
        if current_op == "-":
            return f - s
        if current_op == "*":
            return f * s
        if current_op == "/":
            try:
                return f / s
            except ZeroDivisionError:
                if math.isnan(f):
                    return float('nan')
                if f == 0.0:
                    return float('nan')
                sign_f = math.copysign(1.0, f)
                sign_s = math.copysign(1.0, s)
                if sign_f * sign_s > 0:
                    return float('inf')
                else:
                    return float('-inf')
        if current_op == "%":
            try:
                return math.fmod(f, s)
            except ValueError:
                return float('nan')

        raise ValueError("Unexpected operator: " + current_op)

    @staticmethod
    def transform(expression):
        expr = re.sub(r'\s+', '', expression)
        expr = re.sub(r'=$', '', expr)

        chars = list(expr)
        for i in range(len(chars)):
            if chars[i] == '-':
                if i == 0:
                    chars[i] = '~'
                else:
                    prev_c = chars[i - 1]
                    if prev_c in ('+', '-', '*', '/', '(', 'E', 'e'):
                        chars[i] = '~'

        expr = ''.join(chars)

        if expr and expr[0] == '~' and len(expr) > 1 and expr[1] == '(':
            expr = '-' + expr[1:]
            return "0" + expr
        else:
            return expr

    def prepare(self, expression):
        op_stack = [","]
        arr = expression
        current_index = 0
        count = 0
        self.postfix_stack.clear()

        i = 0
        while i < len(arr):
            current_op = arr[i]

            if self.is_operator(current_op):
                if count > 0:
                    self.postfix_stack.append(arr[current_index:current_index + count])

                peek_op = op_stack[-1]

                if current_op == ")":
                    while op_stack[-1] != "(":
                        self.postfix_stack.append(op_stack.pop())
                    op_stack.pop()
                else:
                    while current_op != "(" and peek_op != "," and self.compare(current_op, peek_op):
                        self.postfix_stack.append(op_stack.pop())
                        peek_op = op_stack[-1]
                    op_stack.append(current_op)

                count = 0
                current_index = i + 1
            else:
                count += 1

            i += 1

        if count > 1 or (count == 1 and not self.is_operator(arr[current_index:current_index + count])):
            self.postfix_stack.append(arr[current_index:current_index + count])

        while op_stack[-1] != ",":
            self.postfix_stack.append(op_stack.pop())

    def calculate(self, expression):
        self.prepare(self.transform(expression))

        result_stack = []

        for current_op in self.postfix_stack:
            if not self.is_operator(current_op):
                current_op = re.sub(r'~', '-', current_op)
                result_stack.append(current_op)
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()

                first_value = re.sub(r'~', '-', first_value)
                second_value = re.sub(r'~', '-', second_value)

                temp_result = self._calculate(first_value, second_value, current_op)
                result_stack.append(to_string_cpp(temp_result))

        result_str = ""
        for val in result_stack:
            result_str += val + "*"
        if result_str:
            result_str = result_str[:-1]

        return stod(result_str)