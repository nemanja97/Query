class Vertex():

    def __init__(self, path):
        self.path = path
        self.incoming_edges = []

    def addEdge(self, other):
        if isinstance(other, Vertex):
            other.incoming_edges.append(self.path)

    def getIncomingEdges(self):
        return self.incoming_edges