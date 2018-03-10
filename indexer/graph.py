from vertex import Vertex


class Graph:

    def __init__(self):
        self.vertices = {}

    def __getitem__(self, item):
        return self.vertices[item]

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex):
            if vertex not in self.vertices:
                self.vertices[vertex.path] = vertex

    def remove_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex in self.vertices:
            del self.vertices[vertex.path]