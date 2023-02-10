import graph as gr


# Maybe offer the user to choose a different way of display
def display_graph(graph_to_display: gr.Graph):
    if graph_to_display is None:
        return "The graph has not been created yet."
    else:
        return graph_to_display.get_matrix()


if __name__ == '__main__':
    running = 1
    active_graph = None
    while running:
        print(display_graph(active_graph))
        print("What action would you like to perform ?")
        print("0. Quit")
        print("1. Create Graph")

        user_input = input()

        match user_input:
            case "0":
                print("Goodbye")
                running = 0
            case "1":
                active_graph = gr.Graph("test.txt")
            case _:
                print("Unknown action")
