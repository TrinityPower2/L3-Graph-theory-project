class Logger:

    def __init__(self, subject_filename):
        self.subject_filename = subject_filename
        self.savefile = open(subject_filename+"-trace.txt", "x")

    def log(self, to_log):
        print(to_log)
        self.savefile.write(to_log)
