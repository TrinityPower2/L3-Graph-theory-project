def has_cycle_plus_ranks(AM, version):
    # 1st version where we don't need to compute the ranks. It uses Roy Warshall algorithm
    if version == 0:
        trans_clos = transition_closure_AM(AM)
        for i in range(0, len(AM)):
            if AM[i][i] != 0:
                return True
        return False
    # 2nd version where we will search for cycles and compute ranks at the same time
    elif version == 1:
        matrix_len = len(AM)
        ranks = {0: ""}
        nb_rk = 0
        change = True
        removed = []
        while change and len(removed) != matrix_len:
            change = False
            to_be_removed = []
            for j in range(0, matrix_len):
                if is_zeros(get_column(AM, j)):
                    if j not in removed:
                        change = True
                        to_be_removed.append(j)
                        removed.append(j)
                        if ranks[nb_rk] == "":
                            ranks[nb_rk] = str(j)
                        else:
                            ranks[nb_rk] = ranks[nb_rk] + " " + str(j)
            if change:
                for col in to_be_removed:
                    for i in range(0, len(AM)):
                        AM[col][i] = 0
                nb_rk += 1
                ranks[nb_rk] = ""
        if len(removed) == matrix_len:
            print("Here are the ranks:\n")
            for i in range(0, len(ranks.keys())):
                if ranks[i] != "":
                    print("rank", i, ":", ranks[i])
            return False
        else:
            return True


def get_column(AM, col_nb):
    col = []
    matrix_len = len(AM)
    for i in range(0, matrix_len):
        col.append(AM[i][col_nb])
    return col


def is_zeros(col):
    for i in col:
        if i != 0:
            return False
    return True


def transition_closure_AM(init_AM):
    closure_AM = init_AM
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


def get_predecessors(AM, vertice_nb):
    length = len(AM)
    results = []
    results_l = 0
    for i in range(0,length):
        if AM[i][vertice_nb] != 0:
            results.append(i)
    return results


def get_successors(AM, vertice_nb):
    length = len(AM)
    results = []
    results_l = 0
    for i in range(0, length):
        if AM[vertice_nb][i] != 0:
            results.append(i)
    return results


AM = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
      [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
AM2 = [[0, 2], [4, 0]]
print(has_cycle_plus_ranks(AM2, 1))
