class Vertex:

    def __init__(self, name: str, duration: int, predecessors):
        self.name = name
        self.duration = duration
        self.predecessors = predecessors
