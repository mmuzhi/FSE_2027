import math
import re
from collections import deque


class ExpressionCalculator:
    _WS_RE = re.compile(r"[ \t\n\v\f\r]+")
    _NUMBER_RE = re.compile(r"[ \t\n\v\f\r]*([+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)")
    _SPECIAL_RE = re.compile(r"[ \t\n\v\f\r]*([+-]?)(inf(?:inity)?|nan)", re.IGNORECASE)
    _OPERATORS = frozenset({"+", "-", "*", "/", "(", ")", "%"})

    def __init__(self):
        self.postfix_stack = deque()
        self.operat_priority = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression):
        self.prepare(self.transform(expression))

        result_stack = deque()
        reversed_postfix_stack = deque(reversed(self.postfix_stack))

        while reversed_postfix_stack:
            current_op = reversed_postfix_stack.pop()

            if not self.is_operator(current_op):
                current_op = current_op.replace("~", "-")
                result_stack.append(current_op)
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()

                first_value = first_value.replace("~", "-")
                second_value = second_value.replace("~", "-")

                temp_result = self._calculate(first_value, second_value, current_op)
                result_stack.append(self._to_string(temp_result))

        result_str = "*".join(result_stack)
        return self._stod(result_str)

    def prepare(self, expression):
        op_stack = deque([","])
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

                if current_op == ")":
                    while op_stack[-1] != "(":
                        self.postfix_stack.append(op_stack[-1])
                        op_stack.pop()
                    op_stack.pop()
                else:
                    while current_op != "(" and peek_op != "," and self.compare(current_op, peek_op):
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

        while op_stack[-1] != ",":
            self.postfix_stack.append(op_stack[-1])
            op_stack.pop()

    @staticmethod
    def is_operator(c):
        return c in ExpressionCalculator._OPERATORS

    def compare(self, cur, peek):
        cur_op = "/" if cur == "%" else cur
        peek_op = "/" if peek == "%" else peek
        return self.operat_priority[ord(peek_op[0]) - 40] >= self.operat_priority[ord(cur_op[0]) - 40]

    @classmethod
    def _calculate(cls, first_value, second_value, current_op):
        f = cls._stod(first_value)
        s = cls._stod(second_value)

        if current_op == "+":
            return f + s
        if current_op == "-":
            return f - s
        if current_op == "*":
            return f * s
        if current_op == "/":
            # IEEE semantics: C++ divides by zero yielding inf/nan instead of raising
            if s == 0:
                if f == 0 or math.isnan(f):
                    return math.nan
                return math.copysign(math.inf, f) * math.copysign(1.0, s)
            return f / s
        if current_op == "%":
            if s == 0:
                return math.nan
            return math.fmod(f, s)

        raise ValueError("Unexpected operator: " + current_op)

    @staticmethod
    def _stod(s):
        # Mimics std::stod: parses longest valid numeric prefix; raises on no conversion,
        # OverflowError on out-of-range (analog of std::out_of_range).
        m = ExpressionCalculator._NUMBER_RE.match(s)
        if m is not None:
            value = float(m.group(1))
            if math.isinf(value):
                raise OverflowError("stod: result out of range")
            return value
        m = ExpressionCalculator._SPECIAL_RE.match(s)
        if m is not None:
            if m.group(2).lower().startswith("inf"):
                return -math.inf if m.group(1) == "-" else math.inf
            return math.nan
        raise ValueError("stod: no conversion ({!r})".format(s))

    @staticmethod
    def _to_string(value):
        # Mimics std::to_string(double): fixed 6 decimal places
        return f"{value:.6f}"

    @staticmethod
    def transform(expression):
        expr = ExpressionCalculator._WS_RE.sub("", expression)
        expr = re.sub("=$", "", expr)

        chars = list(expr)
        for i in range(len(chars)):
            if chars[i] == "-":
                if i == 0:
                    chars[i] = "~"
                else:
                    prev_c = chars[i - 1]
                    if prev_c in "+-*/(Ee":
                        chars[i] = "~"

        if chars[:1] == ["~"] and len(chars) > 1 and chars[1] == "(":
            chars[0] = "-"
            return "0" + "".join(chars)
        return "".join(chars)