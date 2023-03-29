
def has_negative_edge(gr):
    for vex in gr.vertices:
        if vex.duration < 0:
            return True
    return False
