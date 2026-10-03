from collections import deque

class TextEditor:
    def __init__(self):
        self.left = deque()
        self.right = deque()
        
    def addText(self, text: str) -> None:
        for c in text:
            self.right.append(c)
        
    def deleteText(self, k: int) -> int:
        i = 0
        while self.right and i < k:
            self.right.pop()
            i += 1
        return i
        
    def cursorLeft(self, k: int) -> str:
        i = 0
        while self.right and i < k:
            self.left.appendleft(self.right.pop())
            i += 1
        return "".join(self.left) + "".join(self.right)
        
    def cursorRight(self, k: int) -> str:
        i = 0
        while self.left and i < k:
            self.right.appendleft(self.left.popleft())
            i += 1
        return "".join(self.left) + "".join(self.right)