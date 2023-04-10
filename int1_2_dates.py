from tabulate import tabulate
from int1_2_cycle_detection import has_cycle_plus_ranks

"""

GRAPH THEORY PROJECT
L3 - INT1 - Promo 2025 - Group 2
BLAIS Angèle, BRUNIER Léna, CAPELLA Jean-Baptiste, CHRETIENNOT Noam, CRAIPEAU ANTOINE

"""


def get_predecessors(g) -> dict:
    """
        Return a dictionary of type {vertex: [predecessors], ...}
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


def get_ranks_as_2dlist(g, display=False) -> list:
    """
        Return a 2D list of vertices where the index is the rank\n
        using Roy-Warshall algorithm from int1_2_cycle_detection.py Has_cycle_plus_ranks function
    """

    # fetches the ranks of each vertex from the adjacency matrix via the has_cycle_plus_ranks function
    serial_ranks = has_cycle_plus_ranks(g.adjacency_matrix, False)[1]
    ranks = []
    # we create a 2D list of vertices where the index is the rank
    # we therefore create a list per rank
    for i in range(max(serial_ranks) + 1):
        ranks.append([])

    if display:
        g.logger.log("2D List is ready to be filled with vertices id : ", ranks)

    # we fill the 2D list with the vertices id in the graph's list of vertices
    for i in range(len(serial_ranks)):
        ranks[serial_ranks[i]].append(i)

    if display:
        g.logger.log("2D List filled with vertices id : ", ranks)

    return ranks


def earliest_dates(g, display=False) -> list:
    """
    Return the duration to get to each vertex
    """
    ranks = get_ranks_as_2dlist(g)
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
        g.logger.log(tabulate(values, headers=col_headers, tablefmt="grid"))

    return [earliestD[v] for v in sorted(earliestD)]


def latest_dates(g, display=False) -> list:
    """
    Return the latest date for a vertex
    """
    earliestD = earliest_dates(g)
    w = len(g.adjacency_matrix) - 1  # number of vertex the W
    latestD = {w: earliestD[w]}
    ranks = get_ranks_as_2dlist(g)

    for r in range(len(ranks) - 1, -1, -1):  # loop from highest to lowest ranks
        for vertex in ranks[r]:
            earliest_succD = earliestD[w]  # is latest date in the graph

            # minimum "earliest date" in successors -> latest date of latestD[vertex]
            for i in range(w + 1):
                if g.adjacency_matrix[vertex][i] != '*':
                    if earliest_succD > latestD[i] - int(g.adjacency_matrix[vertex][i]):
                        earliest_succD = latestD[i] - int(g.adjacency_matrix[vertex][i])
            latestD[vertex] = earliest_succD

    # print the tabulated version
    if display:
        col_headers = [str(i) for i in range(len(latestD))]
        col_headers[0] = "A"
        col_headers[-1] = "W"
        values = [[str(v) for v in earliestD],
                  [str(latestD[v]) for v in sorted(latestD)]]
        values[0].insert(0, "Earliest dates")
        values[1].insert(0, "Latest dates")
        g.logger.log(tabulate(values, headers=col_headers, tablefmt="grid"))

    return [latestD[v] for v in sorted(latestD)]


def floats(g, display=False) -> list:
    """
    Return the difference between latest dates and earliest_dates
    """
    ranks = has_cycle_plus_ranks(g.adjacency_matrix, False)[1]
    latestD = latest_dates(g)
    earliestD = earliest_dates(g)
    floatD = []

    # difference between the earliest date and latest date for each vertex
    for i in range(len(earliestD)):
        floatD.append(latestD[i] - earliestD[i])

    # print the tabulated version
    if display:
        col_headers = [str(i) for i in range(len(floatD))]
        col_headers[0] = "A"
        col_headers[-1] = "W"
        col_headers.insert(0, "")
        values = [ranks, earliestD.copy(), latestD.copy(), floatD.copy()]
        values[0].insert(0, "Ranks")
        values[1].insert(0, "Earliest Dates")
        values[2].insert(0, "Latest Dates")
        values[3].insert(0, "Floats")

        g.logger.log(tabulate(values, headers=col_headers, tablefmt="grid"))

    return floatD


def critical_path(g, floatd: list, display=False):
    # I assume it has been verified this graph is a scheduling graph (no loops)

    # We turn the floats from a list to a dict using the vertices names as keys
    dict_floats = {}
    for i in range(len(g.vertices)):
        dict_floats[g.vertices[i].name] = floatd[i]

    # The first path is a path starting from A, for now there is only one path left to explore
    paths = [["A"]]
    paths_left = 1

    # While paths_left > 0 (meaning there are still paths not ending with an Omega (W)), we explore the paths
    while paths_left > 0:
        # We take the first path that has not been explored yet
        current_path = paths[len(paths) - paths_left]
        # We take the last vertex of the path
        current_vertex = current_path[-1]

        # We explore the path until we reach the Omega vertex (W)
        while current_vertex != "W":

            # We will explore the successors of the current vertex to see which one(s) has a float of 0
            # next_z will contain the names of the successors with a float of zero
            vertex = g.get_vertex(current_vertex)
            next_z = []

            for successor in vertex.successors:
                if successor.name in dict_floats.keys():
                    if dict_floats[successor.name] == 0:
                        next_z.append(successor.name)

            # If more than one successor has a float = 0, we create a copy of the current path for each extra successor,
            # and we add the successor to the path. We also increment the number of paths left to explore
            for i in range(len(next_z) - 1):
                temp_copy = current_path.copy()
                temp_copy.append(next_z[i + 1])
                paths.append(temp_copy)  # We create a copy to start again from here
                paths_left += 1

            # We add the first successor to the current path, and we set the current vertex to the vertex we just added
            current_path.append((next_z[0]))
            current_vertex = current_path[-1]

        # We have reached the Omega vertex, so we decrement the number of paths left to explore
        paths_left -= 1

    # now we have to take only paths that have a total of values equal to the latest date of W
    latest_date = latest_dates(g)[-1]
    critical_paths = []
    for path in paths:
        total = 0
        for vertex in path:
            total += int(g.get_vertex(vertex).duration)
        if total == latest_date:
            critical_paths.append(path)

    # we print the critical paths found
    if display:
        g.logger.log("\nCritical Paths :")
        result = ""
        for path in critical_paths:
            for vertex in path[:-1]:
                result += vertex + '->'
            result += path[-1]
            result += '\n'
        g.logger.log(result)

        # now we create an array with every unique vertex in paths so we can send it to the graph with highlight
        unique_vertices = []
        for path in critical_paths:
            for vertex in path:
                if vertex not in unique_vertices:
                    unique_vertices.append(vertex)

        edges_to_highlight = []
        for path in critical_paths:
            for i in range(len(path) - 1):
                if (path[i], path[i + 1]) not in edges_to_highlight:
                    edges_to_highlight.append((path[i], path[i + 1]))

        g.graphic_plot_with_highlights(unique_vertices, edges_to_highlight)

    return critical_paths
