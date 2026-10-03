class BalancedBrackets:
    def __init__(self, expr):
        self.stack = []
        self.left_brackets = "({["
        self.right_brackets = ")}]"
        self.expr = expr

    def clear_expr(self):
        cleaned_expr = ''.join(c for c in self.expr if c in self.left_brackets + self.right_brackets)
        self.expr = cleaned_expr

    def check_balanced_brackets(self):
        self.clear_expr()
        for brkt in self.expr:
            if brkt in self.left_brackets:
                self.stack.append(brkt)
            else:
                if not self.stack:
                    return False
                top = self.stack.pop()
                if (top == '(' and brkt != ')') or \
                   (top == '{' and brkt != '}') or \
                   (top == '[' and brkt != ']'):
                    return False
        return len(self.stack) == 0

    def get_expr(self):
        return self.expr

if __name__ == "__main__":
    b = BalancedBrackets("a(b)c")
    print(b.check_balanced_brackets())