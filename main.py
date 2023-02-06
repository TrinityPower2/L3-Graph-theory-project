import graph

import inquirer


def display_graph(graph_to_display: graph):
    if graph_to_display is None:
        return "The graph has not been created yet"
    else:
        return "WIP"


if __name__ == '__main__':
    running = 1
    active_graph = None
    while running:

        print("What action would you like to perform ?")
        print(display_graph(active_graph))
        print("0. Quit")

        user_input = input()

        match user_input:
            case "0":
                print("Goodbye")
                running = 0
            case _:
                print("Unknown action")
