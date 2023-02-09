class Vertex:

    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration
        self.predecessors = []
        self.successors = []
