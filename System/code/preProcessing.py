import argparse


class tokenize(object):
    def __init__(self, lang):
        self.lang = lang
        base = {'as': 0X0980, 'bn': 0X0980, 'gu': 0X0A80, 'hi': 0X0900, 'kn': 0X0C80, 'ml': 0X0D00, 'mr': 0X0900,
                'pa': 0X0A00, 'ta': 0X0B80, 'te': 0X0C00}
        if lang == 'en':
            self.vowels = ['A', 'E', 'I', 'O', 'U', 'a', 'e', 'i', 'o', 'u']
        else:
            self.vowels = [chr(x + base[lang]) for x in
                           [0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006, 0x0007, 0x0008, 0x0009, 0x000A,
                            0x000B, 0x000C, 0x000D, 0x000E, 0x000F, 0x0010, 0x0011, 0x0012, 0x0013, 0x0014, 0x003A,
                            0x003B, 0x003E, 0x003F, 0x0040, 0x0041, 0x0042, 0x0043, 0x0044, 0x0045, 0x0046, 0x0047,
                            0x0048, 0x0049, 0x004A, 0x004B, 0x004C, 0x004E, 0x004F, 0x0055, 0x0056, 0x0057, 0x0062,
                            0x0063]]

    def tokenizer(self, word, OS=True):
        """
        Performs orthographic syllabification on the 'text' string based on 'vowels'
        Arguments:
            :param OS: tokenization method, true: orthographic syllable tokenization; false: character tokenization
            :param word: must contain only akshar combination of a language
            :return: list of orthographic syllables
        """
        word = str(word).strip()
        if not OS:
            return ' '.join(list(word))

        previous_character_vowel = False
        subword = ''
        for char in word:
            if previous_character_vowel and char not in self.vowels:
                previous_character_vowel = False
                subword += ' '
            if char in self.vowels:
                previous_character_vowel = True
            subword += char
        return subword


def cleanData(args):
    DELIM = '\t'
    src = open(args.src, 'r').read().split('\n')
    trg = open(args.trg, 'r').read().split('\n')
    output = open(args.out, 'w')

    source = tokenize(args.src_lang)
    target = tokenize(args.trg_lang)
    for sword, tword in zip(src, trg):
        if sword and tword:
            sword = source.tokenizer(sword, OS=args.char)
            tword = target.tokenizer(tword, OS=args.char)
            output.write(sword + DELIM + tword + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-src_lang', required=True)
    parser.add_argument('-src', required=True)
    parser.add_argument('-trg_lang', required=True)
    parser.add_argument('-trg', required=True)
    parser.add_argument('-out', required=True)
    parser.add_argument('-char', action='store_false')
    args = parser.parse_args()

    cleanData(args)


if __name__ == "__main__":
    main()
