import logger
import vertex as vx
from tabulate import tabulate
import dates as dt
import cycle_detection as cd
import negative_edge_detection as nd
import copy


class Graph:
    def __init__(self, file):

        self.graph_name = file.name.split("/")[-1].split(".")[0]

        self.logger = logger.Logger(self.graph_name)

        # We will store the named vertices in the array, and store the matching predecessors in the dictionary.
        self.vertices = []
        predecessors = {}

        # We add alpha vertex.
        self.vertices.append(vx.Vertex("A", 0))

        # We open the good file and read each line, for each, we store the two first values in the vertex object,
        # and the predecessors in the dictionary using the vertexes name as key.

        for line in file.read().split("\n"):
            line = line.split(" ")
            self.vertices.append(vx.Vertex(line[0], int(line[1])))
            predecessors[line[0]] = line[2:]

        # We add omega vertex.
        self.vertices.append(vx.Vertex("W", 0))

        # Once every vertex has been created, we will fill the successors and predecessors array in each vertex object.
        # We will navigate the dictionary, and fetch the good objects to fill the predecessors and successors.
        # At each get_vertex() call, we verify if output is non-null to avoid crashes.
        for vertex in predecessors.keys():
            temp = self.get_vertex(vertex)
            for predecessor in predecessors.get(vertex):
                temp_predecessor = self.get_vertex(predecessor)
                temp.predecessors.append(temp_predecessor)
                temp_predecessor.successors.append(temp)

        # Adding Alpha predecessor for vertices with no predecessor and Omega successor for vertices with no successor.

        for vertex in self.vertices:
            if not vertex.predecessors and vertex.name != "A" and vertex.name != "W":
                alpha = self.get_vertex("A")
                vertex.predecessors.append(alpha)
                alpha.successors.append(vertex)

            if not vertex.successors and vertex.name != "A" and vertex.name != "W":
                omega = self.get_vertex("W")
                vertex.successors.append(omega)
                omega.predecessors.append(vertex)

        self.adjacency_matrix = []
        self.compute_adjacency_matrix()

    # Loop that will persist while we are observing this graph. When we get out, the graph will be dropped.
    def graph_menu(self):
        self.logger.log("\n==============================")
        self.logger.log("\nCURRENT GRAPH : " + self.graph_name)
        self.logger.log(self.print_adjacency_matrix())
        if cd.has_cycle_plus_ranks(self.adjacency_matrix, True):
            self.logger.log("\nTHIS GRAPH CONTAINS CYCLES AND THEREFORE IS NOT A SCHEDULING GRAPH !\n")
        else:
            if nd.has_negative_edge(self):
                self.logger.log("\nTHIS GRAPH CONTAINS NEGATIVE EDGES AND THEREFORE IS NOT A SCHEDULING GRAPH !\n")
            else:
                self.logger.log("\nTHIS CONTAINS NO CYCLE NOR NEGATIVE EDGES AND THEREFORE IS A SCHEDULING GRAPH !\n")
                dt.critical_path(self, dt.floats(self, display=True), display=True)

    # Allows to get a vertex of the graph from its name.
    def get_vertex(self, name):
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex

        self.logger.log("Vertex " + name + " was not found !")
        raise VertexNotFoundError("Vertex " + name + " was not found !")

    # Allows to display a graph by the successions in a predecessor =length=> successor pattern.
    def get_successions(self):
        output = ""
        for vertex in self.vertices:
            for destination in vertex.successors:
                output += vertex.name + " -> " + destination.name + " = " + str(vertex.duration) + "\n"
        return output

    # Used to compute adjacency matrix from the graph object
    def compute_adjacency_matrix(self):
        # 2D Array that will store the values for each case, including the row headers but excluding the column headers.
        data = []
        # Counter that stores the current row we're at
        cpt = -1
        for vertex in self.vertices:
            # At each new row (vertex), we increment the counter?
            cpt += 1
            # At each new row (vertex), we add a new 1D Array to the 2D Array
            data.append([])
            # At the start of the row, we add a row header, which is the name of the vertex
            for match_vertex in self.vertices:
                # If the vertex of the row has the match_vertex among its successors, we mark the weight of the edge
                # in the matching case, else we put "*"
                if vertex.successors.__contains__(match_vertex):
                    data[cpt].append(str(vertex.duration))
                else:
                    data[cpt].append("*")

        # We return the table made by tabulate from the data and column headers.
        self.adjacency_matrix = data

    # Allow to display the adjacency matrix of the graph
    def print_adjacency_matrix(self):
        # We copy the adjacency matrix to which we will add row headers.
        data = copy.deepcopy(self.adjacency_matrix)
        # Array storing the column headers
        col_headers = []
        # Counter that stores the current row we're at
        cpt = -1
        for vertex in self.vertices:
            # At each new row (vertex), we increment the counter?
            cpt += 1
            # At the start of the row, we add a row header, which is the name of the vertex
            data[cpt].insert(0, vertex.name)
            # Each time we add a new row, we add the matching vertex in the column header list
            col_headers.append(vertex.name)

        # We return the table made by tabulate from the data and column headers.
        return tabulate(data, headers=col_headers, tablefmt="grid")


# Exception to manage cases when a vertex is not found.
class VertexNotFoundError(Exception):
    pass
