import sys
from collections import OrderedDict


def main():
    data_path = "../../data/raw/hi-en/raw."
    file1 = open(data_path + "hi", 'r', encoding='utf-8').read().split()
    file2 = open(data_path + "en", 'r', encoding='utf-8').read().split()

    lang1 = OrderedDict()
    lang2 = OrderedDict()

    for t1, t2 in zip(file1, file2):
        t1 = t1.strip()
        t2 = t2.strip()

        if lang1.get(t1) is None and lang2.get(t2) is None:
            lang1[t1] = t2
            lang2[t2] = t1

    print(len(lang1))
    print(len(lang2))

    with open("test.txt", 'w', encoding='utf-8') as out:
        for k,v in lang1:
            out.write(k+'\t'+v+'\n')

if __name__=="__main__":
     sys.exit(main())