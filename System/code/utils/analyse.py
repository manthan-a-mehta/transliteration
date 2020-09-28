import operator

cmat = dict()
emat = dict()

PATH="/home/cfilt/154054002/parth/OS-NMT/System/data/RUNS/RNN+OS+ATTN/"
prediction_file = ["models/as-en/as-en_128_2_1e-3_200_preds.txt",
                   "models/bn-en/bn-en_128_2_1e-3_100_preds.txt",
                   "models/gu-en/gu-en_256_2_1e-3_300_preds.txt",
                   "../RNN+ATTN/models/hi-en/hi-en_128_2_1e-3_100_preds.txt",
                   "models/kn-en/kn-en_256_2_1e-3_300_preds.txt",
                   "models/ml-en/ml-en_128_2_1e-3_100_preds.txt",
                   "models/mr-en/mr-en_256_2_1e-3_200_preds.txt",
                   "models/pa-en/pa-en_128_2_1e-3_100_preds.txt",
                   "models/ta-en/ta-en_256_2_1e-3_100_preds.txt",
                   "models/te-en/te-en_128_2_1e-3_100_preds.txt"
                   ]
target_file = ["processed/as-en/en-test.txt",
               "processed/bn-en/en-test.txt",
               "processed/gu-en/en-test.txt",
               "processed/hi-en/en-test.txt",
               "processed/kn-en/en-test.txt",
               "processed/ml-en/en-test.txt",
               "processed/mr-en/en-test.txt",
               "processed/pa-en/en-test.txt",
               "processed/ta-en/en-test.txt",
               "processed/te-en/en-test.txt"]

for trg, hyp in zip(target_file, prediction_file):
    with open(PATH+trg, 'r', encoding='utf-8') as target:
        with open(PATH+hyp, 'r', encoding='utf-8') as prediction:
            tag_lines = target.read().split('\n')
            pred_lines = prediction.read().split('\n')

            for tags, preds in zip(tag_lines, pred_lines):

                tag = tags.split(' ')
                pred = preds.split(' ')

                for t, p in zip(tag, pred):
                    if t != p:
                        cmat[t + "::" + p] = cmat.get(t + "::" + p, 0) + 1
                    else:
                        emat[t + "::" + p] = emat.get(t + "::" + p, 0) + 1


cmat = sorted(cmat.items(), key=operator.itemgetter(1))

emat = sorted(emat.items(), key=operator.itemgetter(1))
with open("confusion.txt", 'w') as f:
    f.write(str(cmat))

with open("correct.txt", 'w') as f:
    f.write(str(emat))
