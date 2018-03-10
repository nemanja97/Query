class Stack():
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def isEmpty(self):
        return len(self.data) == 0

    def push(self, element):
        self.data.append(element)

    def top(self):
        if self.isEmpty():
            raise StackError
        else:
            return self.data[-1]

    def pop(self):
        if self.isEmpty():
            raise StackError
        else:
            return self.data.pop()


class StackError(Exception):
    pass