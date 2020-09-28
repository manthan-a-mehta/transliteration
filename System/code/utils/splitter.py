"""
Simple script to split tokens delimited by tab into two different files
"""
import random
import sys

DELIM = '\t'


def writeToFile(lines, SOURCE_FILE, TARGET_FILE):
    for line in lines:
        line.strip()
        if line:
            src, trg = line.split(DELIM)
            SOURCE_FILE.write(src + '\n')
            TARGET_FILE.write(trg + '\n')

    SOURCE_FILE.close()
    TARGET_FILE.close()


def main(args):
    INPUT_FILE = open(args[1], 'r').read().split('\n')
    random.shuffle(INPUT_FILE)

    N = len(INPUT_FILE)
    writeToFile(INPUT_FILE[:N - 4000], open(args[2], 'w'), open(args[3], 'w'))
    writeToFile(INPUT_FILE[N - 4000:N - 2000], open(args[4], 'w'), open(args[5], 'w'))
    writeToFile(INPUT_FILE[N - 2000:], open(args[6], 'w'), open(args[7], 'w'))


if __name__ == "__main__":
    main(sys.argv)
