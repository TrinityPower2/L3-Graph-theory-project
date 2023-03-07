import logger
import vertex as vx
from tabulate import tabulate


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

        # Adding Alpha predecessor for vertices with no predecessor and Omega successor for vertices with no sucessor.

        for vertex in self.vertices:
            if not vertex.predecessors:
                alpha = self.get_vertex("A")
                vertex.predecessors.append(alpha)
                alpha.successors.append(vertex)

            if not vertex.successors:
                omega = self.get_vertex("W")
                vertex.predecessors.append(omega)
                omega.successors.append(vertex)

        self.graph_menu()

    # Loop that will persist while we are observing this graph. When we get out, the graph will be dropped.
    def graph_menu(self):
        running = 1
        while running:
            self.logger.log("\n==============================")
            self.logger.log("\nCURRENT MATRIX : " + self.graph_name)
            self.logger.log(self.get_matrix())
            self.logger.log("\nWhat do you wanna do ? (Press ENTER to return to menu)")
            while 1:
                match (self.logger.log(input())):
                    case "":
                        running = 0
                        break
                    case _:
                        self.logger.log("Unknown command.")

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

    # Allow to display a graph with in a matrix form
    def get_matrix(self):
        # 2D Array that will store the values for each case, including the row headers but excluding the column headers.
        data = []
        # Array storing the column headers
        col_headers = []
        # Counter that stores the current row we're at
        cpt = -1
        for vertex in self.vertices:
            # At each new row (vertex), we increment the counter?
            cpt += 1
            # At each new row (vertex), we add a new 1D Array to the 2D Array
            data.append([])
            # At the start of the row, we add a row header, which is the name of the vertex
            data[cpt].append(vertex.name)
            # Each time we add a new row, we add the matching vertex in the column header list
            col_headers.append(vertex.name)
            for match_vertex in self.vertices:
                # If the vertex of the row has the match_vertex among its successors, we mark the weight of the edge
                # in the matching case, else we put "*"
                if vertex.successors.__contains__(match_vertex):
                    data[cpt].append(str(vertex.duration))
                else:
                    data[cpt].append("*")

        # We return the table made by tabulate from the data and column headers.
        return tabulate(data, headers=col_headers, tablefmt="grid")


# Exception to manage cases when a vertex is not found.
class VertexNotFoundError(Exception):
    pass
