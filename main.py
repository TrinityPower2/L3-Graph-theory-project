from tabulate import tabulate

import graph as gr

# Function to test around tabulate, will be moved later, maybe ...
def display_graph(graph_to_display: gr.Graph):
    if graph_to_display is None:
        data = [["*","0","0","*","*","*","*"],
                ["*","0","0","*","*","*","*"],
                ["*","0","0","*","*","*","*"],
                ["*","0","0","*","*","*","*"],
                ["*","0","0","*","*","*","*"],
                ["*","0","0","*","*","*","*"]]

        col_headers = ["0","1","2","3","4","5","6"]

        a = tabulate(data,headers=col_headers, tablefmt="fancy_grid", showindex="always")
        return "The graph has not been created yet, but anyway:\n" + a
    else:
        return graph_to_display.get_successions()


if __name__ == '__main__':
    running = 1
    active_graph = None
    while running:

        print("What action would you like to perform ?")
        print(display_graph(active_graph))
        print("0. Quit")
        print("1. Create Graph")

        user_input = input()

        match user_input:
            case "0":
                print("Goodbye")
                running = 0
            case "1":
                active_graph = gr.Graph("hello.txt")
            case _:
                print("Unknown action")
