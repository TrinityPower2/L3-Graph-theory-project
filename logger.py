class Logger:

    def __init__(self, subject_filename):
        try:
            self.savefile = open("traces/" + subject_filename+"-trace.txt", "w", encoding="utf-8")
        except FileNotFoundError:
            self.savefile = None
            print("Trace directory not found ! Logging will be discarded !")

    def log(self, to_log):
        print(to_log)
        if self.savefile:
            self.savefile.write(to_log + "\n")
        else:
            print("(Logging is disabled.)")
        return to_log
