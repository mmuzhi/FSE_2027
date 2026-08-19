class BalancedBrackets:
    def __init__(self, expr):
        self.stack = []              # acts as java.util.Stack<Character>
        self.left_brackets = "({["
        self.right_brackets = ")}]"
        self.expr = expr

    def clear_expr(self):
        self.expr = "".join(
            c for c in self.expr
            if self.left_brackets.find(c) != -1 or self.right_brackets.find(c) != -1
        )

    def check_balanced_brackets(self):
        self.clear_expr()
        for brkt in self.expr:
            if self.left_brackets.find(brkt) != -1:
                self.stack.append(brkt)
            else:
                if not self.stack:
                    return False
                current_brkt = self.stack.pop()
                if current_brkt == '(' and brkt != ')':
                    return False
                if current_brkt == '{' and brkt != '}':
                    return False
                if current_brkt == '[' and brkt != ']':
                    return False
        return not self.stack

    def get_expr(self):
        return self.expr


if __name__ == "__main__":
    b = BalancedBrackets("a(b)c")
    print(str(b.check_balanced_brackets()).lower())  # Java prints "true"/"false"