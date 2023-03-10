import os
import sys
import graph as gr

import tkinter as tk
from tkinter import filedialog


def list_graphs():
    print("\nAvailable files:\n")
    for file in os.listdir("graphs/"):
        print("- " + file.split(".")[0])


def file_opener(root_window):
    path = filedialog.askopenfilename(initialdir="./graphs", title="Select a File")
    return path


def main():
    # Creates the tkinter window (necessary to summon the file selector)
    root = tk.Tk()
    if 'linux' in sys.platform:
        root.withdraw()
    else :
        # Hides the tkinter window
        root.wm_attributes('-alpha', 0.0)
        # Disables the tkinter windows' button
        root.wm_attributes('-disabled', True)

    running = 1
    while running:
        print("\nWhat action would you like to perform ?")
        print("0. Quit")
        print("1. Import Graph\n")
        while 1:
            match input():
                case "0":
                    print("Goodbye")
                    running = 0
                    break
                case "1":
                    try:
                        active_graph = gr.Graph(open(file_opener(root), "r"))
                    except gr.VertexNotFoundError:
                        print("A vertex was not found !")
                    except FileNotFoundError:
                        print("Graph file not found !")
                    break
                case _:
                    print("Unknown action")


if __name__ == '__main__':
    main()
