import math
import re

# Mimics C++ std::stod: parses the leading floating-point prefix (or inf/nan).
_STOD_RE = re.compile(
    r'\s*[+-]?(?:(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?|inf(?:inity)?|nan)',
    re.IGNORECASE,
)


def _stod(s):
    m = _STOD_RE.match(s)
    if m is None:
        raise ValueError("stod: no conversion")
    return float(m.group(0))


def _to_string(v):
    # Mimics C++ std::to_string(double) -> "%f" (6 decimal places).
    return f"{v:.6f}"


class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack = []
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression):
        self.prepare(self.transform(expression))

        result_stack = []

        # C++ copies, reverses, and pops from the back -> original front-to-back order.
        for current_op in list(self.postfix_stack):
            if not self.is_operator(current_op):
                current_op = current_op.replace('~', '-')
                result_stack.append(current_op)
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()

                first_value = first_value.replace('~', '-')
                second_value = second_value.replace('~', '-')

                temp_result = self._calculate(first_value, second_value, current_op)
                result_stack.append(_to_string(temp_result))

        # C++ appends "val*" for each element then pops the trailing '*'.
        result_str = '*'.join(result_stack)
        return _stod(result_str)

    def prepare(self, expression):
        op_stack = [',']
        arr = expression
        current_index = 0
        count = 0
        self.postfix_stack.clear()
        for i in range(len(arr)):
            current_op = arr[i]

            if self.is_operator(current_op):
                if count > 0:
                    self.postfix_stack.append(arr[current_index:current_index + count])
                peek_op = op_stack[-1]

                if current_op == ')':
                    while op_stack[-1] != '(':
                        self.postfix_stack.append(op_stack[-1])
                        op_stack.pop()
                    op_stack.pop()
                else:
                    while current_op != '(' and peek_op != ',' and self.compare(current_op, peek_op):
                        self.postfix_stack.append(op_stack[-1])
                        op_stack.pop()
                        peek_op = op_stack[-1]
                    op_stack.append(current_op)

                count = 0
                current_index = i + 1
            else:
                count += 1

        if count > 1 or (count == 1 and not self.is_operator(arr[current_index:current_index + count])):
            self.postfix_stack.append(arr[current_index:current_index + count])

        while op_stack[-1] != ',':
            self.postfix_stack.append(op_stack[-1])
            op_stack.pop()

    @staticmethod
    def is_operator(c):
        return c in ('+', '-', '*', '/', '(', ')', '%')

    def compare(self, cur, peek):
        cur_op = '/' if cur == '%' else cur
        peek_op = '/' if peek == '%' else peek
        return self.operat_priority[ord(peek_op[0]) - 40] >= self.operat_priority[ord(cur_op[0]) - 40]

    @staticmethod
    def _calculate(first_value, second_value, current_op):
        f = _stod(first_value)
        s = _stod(second_value)

        if current_op == '+':
            return f + s
        if current_op == '-':
            return f - s
        if current_op == '*':
            return f * s
        if current_op == '/':
            return f / s
        if current_op == '%':
            return math.fmod(f, s)

        raise ValueError("Unexpected operator: " + current_op)

    @staticmethod
    def transform(expression):
        expr = re.sub(r'[ \t\n\r\f\v]+', '', expression)  # C++ \s is ASCII-only
        expr = re.sub('=$', '', expr)                      # strips one trailing '='

        chars = list(expr)
        for i in range(len(chars)):
            if chars[i] == '-':
                if i == 0:
                    chars[i] = '~'
                else:
                    prev_c = chars[i - 1]
                    if prev_c in '+-*/(Ee':
                        chars[i] = '~'

        if len(chars) > 1 and chars[0] == '~' and chars[1] == '(':
            chars[0] = '-'
            return '0' + ''.join(chars)
        else:
            return ''.join(chars)