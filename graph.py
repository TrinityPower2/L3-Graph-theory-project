import logger
import vertex as vx
from tabulate import tabulate


class Graph:
    def __init__(self, file):

        self.logger = logger.Logger(file.name)

        # We will store the named vertices in the array, and store the matching predecessors in the dictionary.
        self.vertices = []
        predecessors = {}

        # We open the good file and read each line, for each, we store the two first values in the vertex object,
        # and the predecessors in the dictionary using the vertexes name as key.
        for line in file.read().split("\n"):
            line = line.split(" ")
            self.vertices.append(vx.Vertex(line[0], int(line[1])))
            predecessors[line[0]] = line[2:]

        # Once every vertex has been created, we will fill the successors and predecessors array in each vertex object.
        # We will navigate the dictionary, and fetch the good objects to fill the predecessors and successors.
        # At each get_vertex() call, we verify if output is non-null to avoid crashes.
        for vertex in predecessors.keys():
            temp = self.get_vertex(vertex)
            if temp:
                for predecessor in predecessors.get(vertex):
                    temp_predecessor = self.get_vertex(predecessor)
                    if temp_predecessor:
                        temp.predecessors.append(temp_predecessor)
                        temp_predecessor.successors.append(temp)
                    else:
                        self.logger.log("Something went wrong finding temp_predecessor of " + vertex)
            else:
                self.logger.log("Something went wrong finding the vertex named " + vertex)

        self.graph_menu()

    def graph_menu(self):
        running = 1
        while(running):
            self.logger.log("What do you wanna do ?")
            match(input()):
                case 0: running = 0
                case _: self.logger.log("Unknown instruction. Please enter a valid instruction.")

    # Allows to get a vertex of the graph from its name.
    def get_vertex(self, name):
        for vertex in self.vertices:
            if vertex.name == name:
                return vertex

        return None

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
        return tabulate(data, headers=col_headers, tablefmt="fancy_grid")
