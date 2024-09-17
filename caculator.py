# Reference: https://www2.lawrence.edu/fast/GREGGJ/CMSC150/073Calculator/Calculator.html
from stack import Stack

class Caculator:
    values: Stack
    operators: Stack

    def __init__(self) -> None:
        self.values = Stack()
        self.operators = Stack()

    def process(self, raw: list):
        for ch in raw:
            if ch.isdigit():
                # Parse to number
                num = int(ch, 10)
                # Push to stack
                self.values.push(num)
                   
            elif self.__is_operator(ch):
                if self.operators.empty() or self.__get_precedence(ch) > self.__get_precedence(self.operators.peek()):
                    self.operators.push(ch)
                else:
                    while (not self.operators.empty()) and self.__get_precedence(ch) <= self.__get_precedence(self.operators.peek()):
                        # Get peek
                        to_process = self.operators.peek()
                        self.operators.pop()
                        # Process operator
                        self.__process_operator(to_process)

                    self.operators.push(ch)
            elif ch == '(':
                self.operators.push(ch)
            elif ch == ')':
                while (not self.operators.empty()) and self.__is_operator(self.operators.peek()):
                    # Get peek
                    to_process = self.operators.peek()
                    self.operators.pop()
                    # Process operator
                    self.__process_operator(to_process)

                if (not self.operators.empty()) and self.operators.peek() == '(':
                    self.operators.pop()
        
        while (not self.operators.empty()) and self.__is_operator(self.operators.peek()):
            # Get peek
            to_process = self.operators.peek()
            self.operators.pop()
            # Process operator
            self.__process_operator(to_process)

        # Get result
        result = self.values.peek()
        self.values.pop()
        if self.operators.empty() and self.values.empty():
            return result

        return None


    def __process_operator(self, t: str):
        a = 0
        b = 0
        r = 0

        # Get second num
        if not self.values.empty():
            b = self.values.peek()
            self.values.pop()

        # Get first num
        if not self.values.empty():
            a = self.values.peek()
            self.values.pop()

        if t == '+':
            r = a + b
        elif t == '-':
            r = a - b
        elif t == '*':
            r = a * b
        elif t == '/':
            r = a / b

        self.values.push(r)


    def __is_operator(self, ch: str):
        return ch in ["+", "-", "*", "/"]

    def __get_precedence(self, ch: str) -> int:
        if ch in ['+', '-']:
            return 1
        elif ch in ['*', '/']:
            return 2
        
        return 0