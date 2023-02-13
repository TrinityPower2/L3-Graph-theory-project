import os

import graph as gr


def list_graphs():
    for file in os.listdir("graphs/"):
        print("- "+file.split(".")[0])


if __name__ == '__main__':
    running = 1
    while running:
        print("\nWhat action would you like to perform ?")
        print("0. Quit")
        print("1. Import Graph\n")
        while (1):
            match input():
                case "0":
                    print("Goodbye")
                    running = 0
                    break
                case "1":
                    print("\nAvailable files:\n")
                    list_graphs()
                    print("\nPlease enter the name of your file without the extension:")
                    try:
                        active_graph = gr.Graph(open("graphs/" + input() + ".txt", "r"))
                    except FileNotFoundError:
                        print("File not found !")
                    break
                case _:
                    print("Unknown action")
