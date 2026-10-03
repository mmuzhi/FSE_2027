import re
import math
from collections import deque
from typing import List, Deque

class ExpressionCalculator:
    def __init__(self):
        self.postfix_stack: Deque[str] = deque()
        self.operat_priority: List[int] = [0, 3, 2, 1, -1, 1, 0, 2]

    def calculate(self, expression: str) -> float:
        self.prepare(self.transform(expression))

        result_stack: Deque[str] = deque()
        reversed_postfix_stack = self.postfix_stack.copy()
        reversed_postfix_stack.reverse()

        while reversed_postfix_stack:
            current_op = reversed_postfix_stack.pop()

            if not self.is_operator(current_op):
                current_op = current_op.replace('~', '-')
                result_stack.append(current_op)
            else:
                second_value = result_stack.pop()
                first_value = result_stack.pop()

                first_value = first_value.replace('~', '-')
                second_value = second_value.replace('~', '-')

                temp_result = self._calculate(first_value, second_value, current_op)
                result_stack.append(str(temp_result))

        result_str = ''.join(val + '*' for val in result_stack)
        result_str = result_str[:-1]  # remove trailing '*'
        return float(result_str)

    def prepare(self, expression: str) -> None:
        op_stack: Deque[str] = deque([','])
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

                if current_op == ')':
                    while op_stack and op_stack[-1] != '(':
                        self.postfix_stack.append(op_stack.pop())
                    if op_stack and op_stack[-1] == '(':
                        op_stack.pop()
                else:
                    while current_op != '(' and peek_op != ',' and self.compare(current_op, peek_op):
                        self.postfix_stack.append(op_stack.pop())
                        if not op_stack:
                            break
                        peek_op = op_stack[-1]
                    op_stack.append(current_op)

                count = 0
                current_index = i + 1
            else:
                count += 1

            i += 1

        if count > 1 or (count == 1 and not self.is_operator(arr[current_index:current_index + count])):
            self.postfix_stack.append(arr[current_index:current_index + count])

        while op_stack and op_stack[-1] != ',':
            self.postfix_stack.append(op_stack.pop())

    @staticmethod
    def is_operator(c: str) -> bool:
        return c in {'+', '-', '*', '/', '(', ')', '%'}

    def compare(self, cur: str, peek: str) -> bool:
        cur_op = '/' if cur == '%' else cur
        peek_op = '/' if peek == '%' else peek
        idx_cur = ord(cur_op) - 40
        idx_peek = ord(peek_op) - 40
        return self.operat_priority[idx_peek] >= self.operat_priority[idx_cur]

    @staticmethod
    def _calculate(first_value: str, second_value: str, current_op: str) -> float:
        f = float(first_value)
        s = float(second_value)

        if current_op == '+':
            return f + s
        elif current_op == '-':
            return f - s
        elif current_op == '*':
            return f * s
        elif current_op == '/':
            return f / s
        elif current_op == '%':
            return math.fmod(f, s)
        else:
            raise ValueError(f"Unexpected operator: {current_op}")

    @staticmethod
    def transform(expression: str) -> str:
        expr = re.sub(r'\s+', '', expression)
        expr = re.sub(r'=$', '', expr)

        expr_list = list(expr)
        for i in range(len(expr_list)):
            if expr_list[i] == '-':
                if i == 0:
                    expr_list[i] = '~'
                else:
                    prev_c = expr_list[i - 1]
                    if prev_c in ('+', '-', '*', '/', '(', 'E', 'e'):
                        expr_list[i] = '~'
        expr = ''.join(expr_list)

        if len(expr) > 1 and expr[0] == '~' and expr[1] == '(':
            expr = expr.replace('~', '-', 1)  # replace first '~' with '-'
            return "0" + expr
        else:
            return expr