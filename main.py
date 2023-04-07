import os
import sys
import graph as gr

import tkinter as tk
from tkinter import filedialog


def file_opener(root_window):
    path = filedialog.askopenfilename(initialdir="./graphs", title="Select a File")
    # Hides the tkinter window again
    root_window.wm_attributes('-alpha', 0.0)
    # Disables the tkinter windows' button again
    root_window.wm_attributes('-disabled', True)
    return path


def main():
    # Creates the tkinter window (necessary to summon the file selector)
    root = tk.Tk()
    if 'linux' in sys.platform:
        root.withdraw()
    else:
        # Hides the tkinter window
        root.wm_attributes('-alpha', 0.0)
        # Disables the tkinter windows' button
        root.wm_attributes('-disabled', True)

    running = 1
    while running:
        print("\nWhat action would you like to perform ?")
        print("0. Quit")
        print("1. Import Graph")
        print("2. Grand Tour\n")
        while 1:
            user_input = input()
            if user_input == "0":
                print("Goodbye")
                running = 0
                break
            elif user_input == "1":
                try:
                    active_graph = gr.Graph(open(file_opener(root), "r"))
                    active_graph.graph_menu()
                    del active_graph
                    break
                except gr.VertexNotFoundError:
                    print("A vertex was not found !")
                    break
                except FileNotFoundError:
                    print("Graph file not found !")
                    break
            elif user_input == "2":
                print("\nPerforming Grand Tour of test files...")
                for file in os.listdir("graphs/"):
                    try:
                        active_graph = gr.Graph(open("graphs/" + file, "r"), file.split(".")[0] == "table1")
                        active_graph.graph_menu()
                        del active_graph
                    except gr.VertexNotFoundError:
                        print("A vertex was not found !")
                        break
                    except FileNotFoundError:
                        print("Graph file not found !")
                        break

                break


if __name__ == '__main__':
    main()
