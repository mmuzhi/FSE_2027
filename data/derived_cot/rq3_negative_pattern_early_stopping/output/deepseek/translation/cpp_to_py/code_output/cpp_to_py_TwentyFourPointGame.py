import random
import time
import math
import re
from typing import List, Dict, Tuple

class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: math.pow(x, y)
        }

    def precedence(self, op: str) -> int:
        if op in '+-':
            return 1
        elif op in '*/':
            return 2
        elif op == '^':
            return 3
        else:
            return 0

    def apply_operator(self, operand_stack: List[float], operator_stack: List[str]) -> Tuple[List[float], List[str]]:
        op = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()
        result = self.operators[op](operand1, operand2)
        operand_stack.append(result)
        return operand_stack, operator_stack

    def calculate(self, expression: str) -> float:
        if not expression:
            return 0.0

        operand_stack: List[float] = []
        operator_stack: List[str] = []
        num_buffer = ""

        for ch in expression:
            if ch.isdigit() or ch == '.':
                num_buffer += ch
            else:
                if num_buffer:
                    operand_stack.append(float(num_buffer))
                    num_buffer = ""
                if ch in '+-*/^':
                    while (operator_stack and operator_stack[-1] != '(' and
                           self.precedence(operator_stack[-1]) >= self.precedence(ch)):
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.pop()  # remove '('

        if num_buffer:
            operand_stack.append(float(num_buffer))

        while operator_stack:
            operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0


class TwentyFourPointGame:
    def __init__(self):
        self.nums: List[int] = []
        random.seed(time.time())

    def generate_cards(self):
        self.nums = [random.randint(1, 9) for _ in range(4)]

    def get_my_cards(self) -> List[int]:
        self.nums.clear()
        self.generate_cards()
        return list(self.nums)

    def set_nums(self, now: List[int]):
        self.nums = now

    def answer(self, expression: str) -> List[int]:
        if expression == "pass":
            return self.get_my_cards()

        statistic: Dict[str, int] = {}
        for ch in expression:
            if ch.isdigit() and (int(ch) in self.nums):
                statistic[ch] = statistic.get(ch, 0) + 1

        nums_used = dict(statistic)

        for num in self.nums:
            digit_char = str(num)
            if digit_char in nums_used and nums_used[digit_char] > 0:
                nums_used[digit_char] -= 1
            else:
                return []

        if all(v == 0 for v in nums_used.values()):
            if self.evaluate_expression(expression):
                return [1]
            else:
                return []
        else:
            return []

    def evaluate_expression(self, expression: str) -> bool:
        try:
            if not (expression[0].isdigit() or expression[0] == '('):
                raise False
            last_idx = len(expression) - 1
            if not (expression[last_idx].isdigit() or expression[last_idx] == ')'):
                raise False
            calculator = Calculator()
            ans = calculator.calculate(expression)
            return ans == 24.0
        except:
            return False