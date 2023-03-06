class Logger:

    def __init__(self, subject_filename):
        try:
            self.savefile = open("traces/" + subject_filename+"-trace.txt", "w", encoding="utf-8")
        except FileNotFoundError:
            print("Trace directory not found !")

    def log(self, to_log):
        print(to_log)
        self.savefile.write(to_log + "\n")
        return to_log
