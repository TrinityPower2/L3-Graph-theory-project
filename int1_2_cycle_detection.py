import copy     # Library containing the deepcopy function

"""

GRAPH THEORY PROJECT
L3 - INT1 - Promo 2025 - Group 2
BLAIS Angèle, BRUNIER Léna, CAPELLA Jean-Baptiste, CHRETIENNOT Noam, CRAIPEAU ANTOINE

"""


def has_cycle_plus_ranks(adj_mat, version: bool):
    """
    :param adj_mat: the adjacency matrix (square string matrix)
    :param version: tells which version of the function use (the one with only cycle detection or the one with ranks)
    :return: either return a single boolean or a tuple containing a boolean and a dictionary containing the ranks
    """

    AM_copy = copy.deepcopy(adj_mat)     # Avoid to modify the matrix outside the function
    # 1st version where we don't need to compute the ranks. It uses Roy Warshall algorithm
    if version:
        trans_clos = transition_closure_AM(AM_copy)      # We compute the transitive closure of the matrix
        for i in range(0, len(AM_copy)):     # We check if there are 1 on the diagonal of the transitive closure.
            # If yes, we have a cycle
            if trans_clos[i][i] != '*':
                return True
        return False
    # 2nd version where we will search for cycles and compute ranks at the same time
    else:
        matrix_len = len(AM_copy)
        ranks = {0: []}     # Will be used to store the ranks
        nb_rk = 0
        change = True
        removed = []        # Will be used to store the vertices we remove
        while change and len(removed) != matrix_len:    # We stop either when we get no changes or when we removed all
            # vertices
            change = False
            to_be_removed = []
            for j in range(0, matrix_len):
                if is_zeros(get_column(AM_copy, j)):    # If a vertex has its column in the matrix with only 0,
                    # we remove it
                    if j not in removed:
                        change = True
                        to_be_removed.append(j)
                        removed.append(j)
                        ranks[nb_rk].append(j)    # The vertex removed will be assigned its rank with the value of nb_rk
            if change:      # If we removed one or several columns, we need to update the matrix and the value of nb_rk
                for col in to_be_removed:
                    for i in range(0, len(AM_copy)):
                        AM_copy[col][i] = '*'
                nb_rk += 1
                ranks[nb_rk] = []
        if len(removed) == matrix_len:      # At the end, if we removed all the vertices, it means we have no cycles
            ranks.pop(nb_rk)
            ranks_good_format = []          # Return the ranks in a format easy to read by the other functions
            for i in range(matrix_len):
                ranks_good_format.append("")
            for i in ranks:
                for j in ranks[i]:
                    ranks_good_format[j] = i
            return False, ranks_good_format
        else:
            return True


def get_column(adj_mat, col_nb):         # return the column in the matrix of a given vertex
    col = []
    matrix_len = len(adj_mat)
    for i in range(0, matrix_len):
        col.append(adj_mat[i][col_nb])
    return col


def is_zeros(col):                  # check if a given column has only zeros in it
    for i in col:
        if i != '*':
            return False
    return True


def transition_closure_AM(initial_adj_mat):      # compute the transitive closure of a given matrix
    closure_AM = initial_adj_mat
    length = len(closure_AM)
    for i in range(0, length):
        predec = get_predecessors(closure_AM, i)
        succes = get_successors(closure_AM, i)
        predec_l = len(predec)
        succes_l = len(succes)
        for j in range(0, predec_l):
            for k in range(0, succes_l):
                closure_AM[predec[j]][succes[k]] = 1
    return closure_AM


def get_predecessors(adj_mat, vertice_nb):       # Get all the predecessors of a given vertex using a given matrix
    length = len(adj_mat)
    results = []
    for i in range(0, length):
        if adj_mat[i][vertice_nb] != '*':
            results.append(i)
    return results


def get_successors(adj_mat, vertice_nb):         # Get all the successors of a given vertex using a given matrix
    length = len(adj_mat)
    results = []
    for i in range(0, length):
        if adj_mat[vertice_nb][i] != '*':
            results.append(i)
    return results
