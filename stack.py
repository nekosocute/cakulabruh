from node import Node


class Stack:
    top: Node

    def __init__(self) -> None:
        self.top = None

    def push(self, x: str | int) -> None:
        # Create node
        item = Node(x)
        item.next = self.top
        self.top = item

    def pop(self) -> Node:
        self.top = self.top.next

    def empty(self) -> bool:
        return self.top == None

    def peek(self) -> str | int:
        return self.top.value
