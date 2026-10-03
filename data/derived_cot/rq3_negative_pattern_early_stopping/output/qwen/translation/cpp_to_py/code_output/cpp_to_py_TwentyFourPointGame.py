import random
import re
from collections import defaultdict
from typing import List, Tuple, Dict, Optional, Union

class Calculator:
    def __init__(self):
        self.operators = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y,
            '^': lambda x, y: x ** y
        }

    def calculate(self, expression: str) -> float:
        if not expression:
            return 0.0

        tokens = re.findall(r'(\d*\.\d*|\d+|[+\-*/^()])', expression)
        if not tokens:
            return 0.0

        operand_stack = []
        operator_stack = []
        num_buffer = ''

        for ch in expression:
            if ch.isdigit() or ch == '.':
                num_buffer += ch
            else:
                if num_buffer:
                    operand_stack.append(float(num_buffer))
                    num_buffer = ''
                if ch in '+-*/^':
                    while operator_stack and operator_stack[-1] != '(' and self.precedence(operator_stack[-1]) >= self.precedence(ch):
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    operator_stack.append(ch)
                elif ch == '(':
                    operator_stack.append(ch)
                elif ch == ')':
                    while operator_stack and operator_stack[-1] != '(':
                        operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)
                    if operator_stack and operator_stack[-1] == '(':
                        operator_stack.pop()

        if num_buffer:
            operand_stack.append(float(num_buffer))

        while operator_stack:
            operand_stack, operator_stack = self.apply_operator(operand_stack, operator_stack)

        return operand_stack[-1] if operand_stack else 0.0

    def precedence(self, op: str) -> int:
        if op in '+-':
            return 1
        elif op in '*/':
            return 2
        elif op == '^':
            return 3
        return 0

    def apply_operator(self, operand_stack: List[float], operator_stack: List[str]) -> Tuple[List[float], List[str]]:
        if not operator_stack:
            return operand_stack, operator_stack

        op = operator_stack.pop()
        if len(operand_stack) < 2:
            raise ValueError("Invalid expression")

        operand2 = operand_stack.pop()
        operand1 = operand_stack.pop()

        result = self.operators[op](operand1, operand2)
        operand_stack.append(result)
        return operand_stack, operator_stack

class TwentyFourPointGame:
    def __init__(self):
        self.nums = []
        random.seed()

    def generate_cards(self):
        self.nums = [random.randint(1, 9) for _ in range(4)]
        assert len(self.nums) == 4

    def get_my_cards(self) -> List[int]:
        self.generate_cards()
        return self.nums.copy()

    def answer(self, expression: str) -> List[int]:
        if expression == "pass":
            return self.get_my_cards()

        expr_str = expression
        if not expr_str:
            return []

        # Check if expression uses exactly the numbers in self.nums
        num_to_char = {num: str(num) for num in self.nums}
        char_to_num = {char: num for num, char in num_to_char.items()}

        # Count occurrences of each digit in the expression
        expr_digits = defaultdict(int)
        for char in expr_str:
            if char.isdigit():
                num = int(char)
                if num not in self.nums:
                    return []
                expr_digits[char] += 1

        # Check if all required numbers are used at least once
        for num in self.nums:
            if str(num) not in expr_digits or expr_digits[str(num)] < 1:
                return []

        # Evaluate the expression
        try:
            calculator = Calculator()
            result = calculator.calculate(expression)
            return [1] if abs(result - 24) < 1e-10 else []
        except Exception:
            return []

    def set_nums(self, now: List[int]):
        self.nums = now