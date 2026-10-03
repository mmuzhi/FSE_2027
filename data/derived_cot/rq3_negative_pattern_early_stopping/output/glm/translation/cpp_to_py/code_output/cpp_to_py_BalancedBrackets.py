class BalancedBrackets:
    def __init__(self, expr):
        self.stack = []
        self.leftBrackets = "({["
        self.rightBrackets = ")}]"
        self.expr = expr

    def clearExpr(self):
        self.expr = ''.join(
            c for c in self.expr 
            if c in self.leftBrackets or c in self.rightBrackets
        )

    def check_balanced_brackets(self):
        self.clearExpr()
        for Brkt in self.expr:
            if Brkt in self.leftBrackets:
                self.stack.append(Brkt)
            else:
                if not self.stack:
                    return False
                Current_Brkt = self.stack[-1]
                self.stack.pop()
                if Current_Brkt == '(' and Brkt != ')':
                    return False
                if Current_Brkt == '{' and Brkt != '}':
                    return False
                if Current_Brkt == '[' and Brkt != ']':
                    return False
        return not self.stack