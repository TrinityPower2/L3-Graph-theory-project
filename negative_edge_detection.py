
def has_negative_edge(gr):                  # Check if the graph contains negative edges
    for vex in gr.vertices:         # Browse through all the vertices of the graph
        if vex.duration < 0:        # Check that the duration is not negative
            return True
    return False                    # Return false if no negative duration found
