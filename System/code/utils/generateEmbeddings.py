import sys
from gensim.models.fasttext import FastText


def main(args):
    """
    :param args:
        args[1]: Input File
        args[2]: Vector Size
        args[3]: SRC Output File
        args[4]: TRG Output File
    :return: None
    """

    with open(args[1], 'r', encoding='utf-8') as file:
        src_tokens = list()
        trg_tokens = list()
        lines = file.read().split('\n')

        for line in lines:
            if line:
                tokens = line.strip().split('\t')
                src_tokens.append(tokens[0].split(' '))
                trg_tokens.append(tokens[1].split(' '))

        src_model = FastText(sentences=src_tokens, size=int(args[2]), window=3, workers=18, sg=1)
        src_model.build_vocab(src_tokens, update=True)
        src_model.train(src_tokens, total_examples=src_model.corpus_count, epochs=100)
        src_model.wv.save_word2vec_format(args[3])

        trg_model = FastText(sentences=trg_tokens, size=int(args[2]), window=2, workers=18, sg=1)
        trg_model.build_vocab(trg_tokens, update=True)
        trg_model.train(trg_tokens, total_examples=trg_model.corpus_count, epochs=100)
        trg_model.wv.save_word2vec_format(args[4])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
