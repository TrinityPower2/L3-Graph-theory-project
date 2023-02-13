import graph as gr


# Maybe offer the user to choose a different way of display
def display_graph(graph_to_display: gr.Graph):
    if graph_to_display is None:
        return "No graph has been imported yet."
    else:
        return graph_to_display.get_matrix()


if __name__ == '__main__':
    running = 1
    active_graph = None
    while running:
        print(display_graph(active_graph))
        print("\nWhat action would you like to perform ?")
        print("0. Quit")
        print("1. Import Graph\n")

        user_input = input()

        match user_input:
            case "0":
                print("Goodbye")
                running = 0
            case "1":
                print("Please enter the name of your file without the extension:")
                try:
                    file = open(input()+".txt", "r")
                    active_graph = gr.Graph(file)
                except FileNotFoundError:
                    print("File not found !")
            case _:
                print("Unknown action")
