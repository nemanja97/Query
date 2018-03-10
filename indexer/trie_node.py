class Node:
    def __init__(self, letter = ""):
        self.letter = letter
        self.data = None
        self.children = {}

    def addChild(self, key):
        self.children[key] = Node(key)

    def __getitem__(self, key):
        return self.children[key]