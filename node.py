class Node:
    value: str | int
    next = None

    def __init__(self, value: str | int) -> None:
        self.value = value
        self.next = None
