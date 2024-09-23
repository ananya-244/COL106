class Stack:
    def __init__(self) -> None:
        self.st = []

    def push(self, item):
        self.st.append(item)

    def pop(self):
        if not self.is_empty():
            self.st.pop()

    def top(self):
        if not self.is_empty():
            return self.st[-1]

    def is_empty(self):
        if len(self.st) == 0:
            return True
        return False

    def show(self):
        return list(self.st)

        #YOU CAN (AND SHOULD!) MODIFY THIS FUNCTION

    # You can implement this class however you like