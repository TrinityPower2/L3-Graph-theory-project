import graph


def get_predecessors(g) -> dict:
    """
    Return a dictionnary of type {vertex: [predecessors], ...}
    """
    predecessors = {}

    n_vertices = len(g.adjacency_matrix)

    for i in range(n_vertices):
        predecessors[i] = []
    for r in range(n_vertices) :
        for c in range(n_vertices):
            if g.adjacency_matrix[r][c] != '*':
                predecessors[c].append(r)

    return predecessors


def get_ranks(g, display=False) -> list:
        """
        Return a 2D list of vertices where the index is the rank\n
        using Roy-Warshall algorithm
        """
        predecessors = get_predecessors(g)
        n_vertices = len(g.adjacency_matrix)
        
        
        ranks = []
        n = 0
        while len(predecessors) > 0:
            if display == True:
                print("\nstates : ", predecessors)
                
            toDelete = []
            for v in predecessors.keys():
                if len(predecessors[v]) == 0:
                    toDelete.append(v)

            ranks.append(toDelete)
            for td in toDelete:
                for i in range(n_vertices):
                    if g.adjacency_matrix[td][i] != '*':
                        predecessors[i].remove(td)
                del predecessors[td]    

            if display == True: 
                print("rank ", n, " : ", ranks[-1])
                n += 1
        return ranks


def get_durations(g, display=False) -> dict:
    """
    Return the duration to get to each vertex
    """
    ranks = get_ranks(g)
    predecessors = get_predecessors(g)
    durations = {0:0}

    for rv in ranks[1:]:
        for vertex in rv:
            durations[vertex] = durations[predecessors[vertex][0]] + int(g.adjacency_matrix[predecessors[vertex][0]][vertex])
            for p in predecessors[vertex]:
                if int(g.adjacency_matrix[p][vertex]) + durations[p] > durations[predecessors[vertex][0]] :
                    durations[vertex] = int(g.adjacency_matrix[p][vertex]) + durations[p]
    return durations


def earliest_date(g, vertex=-1, display=False) -> int:
    """
    Return the earliest date for a vertex
    """
    durations = get_durations(g, display=display)

    if vertex == -1:
        return durations[len(g.adjacency_matrix)-1]
    else:
        return durations[vertex]


def latest_date(g, display = False) -> dict:
    """Return the latest date for a vertex"""
    earliestD = get_durations(g, display)
    print(earliestD)
    w = len(g.adjacency_matrix)-1
    maxD = {w:earliestD[w]}
    
    ranks = get_ranks(g)
    for r in range(len(ranks)-1,-1,-1):
        for vertex in ranks[r]:
            earliest_succD = earliestD[w]
            for i in range(w+1):
                if g.adjacency_matrix[vertex][i] != '*':
                    if earliest_succD > maxD[i] - int(g.adjacency_matrix[vertex][i]):
                        earliest_succD = maxD[i] - int(g.adjacency_matrix[vertex][i])
            maxD[vertex] = earliest_succD
    return maxD
    
def floats(g, display = False) -> dict:
    latestD= latest_date(g, display= False)
    earliestD= get_durations(g, display=False)
    for v in earliest_date:
        float[v]= earliestD[v]- latestD[v]
    print(float)
    return float