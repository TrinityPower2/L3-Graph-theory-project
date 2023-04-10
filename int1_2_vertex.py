"""

GRAPH THEORY PROJECT
L3 - INT1 - Promo 2025 - Group 2
BLAIS Angèle, BRUNIER Léna, CAPELLA Jean-Baptiste, CHRETIENNOT Noam, CRAIPEAU ANTOINE

"""


class Vertex:

    def __init__(self, name: str, duration: int):
        # string name of the vertex
        self.name = name
        # int duration of the vertex
        self.duration = duration
        # list of references of predecessors
        self.predecessors = []
        # list of references of successors
        self.successors = []
