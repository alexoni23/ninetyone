# to run:
#.../python> top_scorers.py -i TestData.csv


import sys
import getopt
import os


class FileAsStringExtractor(object):
    def __init__(self, file_name):
        self.file_name = file_name

    def process_next(self):
        with open(self.file_name, "r") as file:
            data = file.read()
        for line in data.split('\n'):
        # for line in open(self.file_name, "r"): <- this is a more 'pythonic' way than 3 line above
            yield line


class TopScoreTransformer(object):
    def __init__(self, source, sep):
        self.source = source
        self.score = -1
        self.scorers = None
        self.sep = sep

    def process_next(self):
        for data in self.source.process_next():
            t = data.strip().split(self.sep)
            if len(t) != 3 or (not t[2].isnumeric()):
                continue  # log an error here or throw an exception
            score = int(t[2])
            scorer = " ".join(t[:2])
            if score == self.score:
                self.scorers.append(scorer)
            elif score > self.score:
                self.score = score
                self.scorers = [scorer]
        assert self.scorers, "failed to find any scorers"
        scorers = sorted(self.scorers)
        yield scorers + [f"Score: {self.score}"]


class PrintOutputLoader(object):
    def __init__(self, source):
        self.source = source

    def process_next(self):
        for data in self.source.process_next():
            _ = [print(s) for s in data]
            yield 0


def main(argv):
    inputfile = ''
    separator = ","
    opts, args = getopt.getopt(argv, "i:s:", ["ifile=", "separator="])
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
        if opt in ("-s", "--separator"):
            separator = arg

    if not inputfile:
        print('top_scorers.py -i <inputfile> -s <column_separator>')
        sys.exit(1)

    input_dir = "."
    fn = os.path.join(input_dir, inputfile)

    E = FileAsStringExtractor(fn)
    T = TopScoreTransformer(E, separator)
    L = PrintOutputLoader(T)

    for _ in L.process_next():
        pass

    return 0


if __name__ == "__main__":
    main(sys.argv[1:])
