import vertex as vx
from tabulate import tabulate


class Graph:
    def __init__(self, filename: str):

        # We will store the named vertices in the array, and store the matching predecessors in the dictionary.
        self.vertices = []
        predecessors = {}

        # We open the good file and read each line, for each, we store the two first values in the vertex object,
        # and the predecessors in the dictionary using the vertexes name as key.
        f = open(filename, "r")
        for line in f.read().split("\n"):
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
                        print("Something went wrong finding temp_predecessor of " + vertex)
            else:
                print("Something went wrong finding the vertex named " + vertex)

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

    def get_matrix(self):
        data = []
        col_headers = []
        cpt = -1
        for vertex in self.vertices:
            cpt += 1
            data.append([])
            data[cpt].append(vertex.name)
            col_headers.append(vertex.name)
            for match_vertex in self.vertices:
                if vertex.successors.__contains__(match_vertex):
                    data[cpt].append(str(vertex.duration))
                else:
                    data[cpt].append("*")

        a = tabulate(data, headers=col_headers, tablefmt="fancy_grid")

        return a
