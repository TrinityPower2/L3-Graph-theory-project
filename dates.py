import graph as gr
from tabulate import tabulate


def get_predecessors(g) -> dict:
    """
    Return a dictionnary of type {vertex: [predecessors], ...}
    """
    predecessors = {}
    n_vertices = len(g.adjacency_matrix)  # number of vertices

    # generate structure of predecessors
    for i in range(n_vertices):
        predecessors[i] = []

    # for each vertex
    for r in range(n_vertices):
        for c in range(n_vertices):
            if g.adjacency_matrix[r][c] != '*':  # if c in successors of r
                predecessors[c].append(r)  # add vertex r to predecessors of c

    return predecessors


def get_ranks(g, display=False) -> list:
    """
        Return a 2D list of vertices where the index is the rank\n
        using Roy-Warshall algorithm
        """
    predecessors = get_predecessors(g)
    n_vertices = len(g.adjacency_matrix)  # number of vertices

    ranks = []
    n = 0  # counter for the rank (if display)
    while len(predecessors) > 0:  # until no vertex is left
        if display == True:
            print("\nRemaining vertices : ", predecessors)

        # acknoledge vertices that have no predecessors
        toDelete = []
        for v in predecessors.keys():
            if len(predecessors[v]) == 0:
                toDelete.append(v)

        ranks.append(toDelete)  # ranks

        for td in toDelete:
            for i in range(n_vertices):
                if g.adjacency_matrix[td][i] != '*':
                    predecessors[i].remove(td)  # delete useless edges
            del predecessors[td]  # delete vertex

        if display == True:
            print("Vertices of rank ", n, " : ", ranks[-1])
            n += 1

    return ranks


def earliest_dates(g, display=False) -> list:
    """
    Return the duration to get to each vertex
    """
    ranks = get_ranks(g)
    predecessors = get_predecessors(g)
    earliestD = {0: 0}

    for rv in ranks[1:]:
        for vertex in rv:
            # maximum("earliest date" in predecessors + duration of edge) -> earliest date of vertex
            earliestD[vertex] = earliestD[predecessors[vertex][0]]
            earliestD[vertex] += int(g.adjacency_matrix[predecessors[vertex][0]][vertex])
            for p in predecessors[vertex][1:]:
                if int(g.adjacency_matrix[p][vertex]) + earliestD[p] > earliestD[vertex]:
                    earliestD[vertex] = int(g.adjacency_matrix[p][vertex]) + earliestD[p]

    # print the tabulated version
    if display:
        col_headers = [str(i) for i in range(len(earliestD))]
        col_headers[0] = "A"
        col_headers[-1] = "W"
        values = [[str(earliestD[v]) for v in sorted(earliestD)]]
        values[0].insert(0, "Earliest dates")
        print(tabulate(values, headers=col_headers, tablefmt="grid"))

    return [earliestD[v] for v in sorted(earliestD)]


def latest_dates(g, display=False) -> list:
    """
    Return the latest date for a vertex
    """
    earliestD = earliest_dates(g)
    w = len(g.adjacency_matrix) - 1  # number of vertex the W
    latestD = {w: earliestD[w]}
    ranks = get_ranks(g)

    for r in range(len(ranks) - 1, -1, -1):  # loop from highest to lowest ranks
        for vertex in ranks[r]:
            earliest_succD = earliestD[w]  # is latest date in the graph

            # minimum "earliest date" in successors -> latest date of latestD[vertex]
            for i in range(w + 1):
                if g.adjacency_matrix[vertex][i] != '*':
                    if earliest_succD > latestD[i] - int(g.adjacency_matrix[vertex][i]):
                        earliest_succD = latestD[i] - int(g.adjacency_matrix[vertex][i])
            latestD[vertex] = earliest_succD

    # print the tabulate version
    if display:
        col_headers = [str(i) for i in range(len(latestD))]
        col_headers[0] = "A"
        col_headers[-1] = "W"
        values = [[str(v) for v in earliestD],
                  [str(latestD[v]) for v in sorted(latestD)]]
        values[0].insert(0, "Earliest dates")
        values[1].insert(0, "Latest dates")
        print(tabulate(values, headers=col_headers, tablefmt="grid"))

    return [latestD[v] for v in sorted(latestD)]


def floats(g, display=False) -> list:
    """
    Return the difference between latest dates and earliest_dates
    """
    latestD = latest_dates(g)
    earliestD = earliest_dates(g)
    floatD = []

    # difference between earliest date and latest date for each vertex
    for i in range(len(earliestD)):
        floatD.append(latestD[i] - earliestD[i])

    # print the tabulate version
    if display:
        col_headers = [str(i) for i in range(len(floatD))]
        col_headers[0] = "A"
        col_headers[-1] = "W"
        col_headers.insert(0, "")
        values = [earliestD.copy(), latestD.copy(), floatD.copy()]
        values[0].insert(0, "Earliest Dates")
        values[1].insert(0, "Latest Dates")
        values[2].insert(0, "Floats")

        g.logger.log(tabulate(values, headers=col_headers, tablefmt="grid"))

    return floatD


def critical_path(g, floatd: list, display=False):
    # I assume it has been verified thig graph is schedulable (no loops)
    dict_floats = {}

    for i in range(len(g.vertices)):
        dict_floats[g.vertices[i].name] = floatd[i]

    paths = [["A"]]
    paths_left = 1

    while paths_left > 0:
        current_path = paths[len(paths) - paths_left]
        current_vertex = current_path[-1]
        while current_vertex != "W":
            vertex = g.get_vertex(current_vertex)
            nexts = []

            for successor in vertex.successors:
                if successor.name in dict_floats.keys():
                    if dict_floats[successor.name] == 0:
                        nexts.append(successor.name)

            for i in range(len(nexts) - 1):
                temp_copy = current_path.copy()
                temp_copy.append(nexts[i + 1])
                paths.append(temp_copy)  # We create a copy to start again from here
                paths_left += 1

            current_path.append((nexts[0]))
            current_vertex = current_path[-1]

        paths_left -= 1

    if display:
        g.logger.log("Critical Paths :")
        result = ""
        for path in paths:
            for vertex in path[:-1]:
                result += vertex + '->'
            result += path[-1]
            result += '\n'
        g.logger.log(result)

    return paths
