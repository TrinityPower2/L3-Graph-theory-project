"""

GRAPH THEORY PROJECT
L3 - INT1 - Promo 2025 - Group 2
BLAIS Angèle, BRUNIER Léna, CAPELLA Jean-Baptiste, CHRETIENNOT Noam, CRAIPEAU ANTOINE

"""


class Logger:

    def __init__(self, subject_filename):
        try:
            # Try to open the file in which we will log the traces
            # If the directory does not exist, we will not log anything
            # If we do not have the permission to write in the directory, we will not log anything
            # If an unknown error occurs, we will not log anything
            self.savefile = open("traces/" + subject_filename+"-trace.txt", "w", encoding="utf-8")
        except FileNotFoundError:
            self.savefile = None
            print("Trace directory not found ! Logging will be discarded !")
        except PermissionError:
            self.savefile = None
            print("Permission denied ! Logging will be discarded !")
        except Exception:
            self.savefile = None
            print("An unknown error occurred ! Logging will be discarded !")

    def log(self, to_log):
        # Act as a print function, but also log the message in a file
        # If the file opening failed, we will not log anything
        print(to_log)
        if self.savefile:
            self.savefile.write(to_log + "\n")
        else:
            print("(Logging is disabled.)")
        return to_log
