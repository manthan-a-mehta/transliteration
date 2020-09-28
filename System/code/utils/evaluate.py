import sys

# TODO: Further refine the logic


def accuracy(target_file, prediction_file, OS=True):
    """
    :param target_file: Name of the target file
    :param prediction_file: Name of the prediction file
    :param OS: Default True, whether to compare OS or Char
    :return: Prints Accuracy
    """

    with open(target_file, 'r', encoding='utf-8') as target:
        with open(prediction_file, 'r', encoding='utf-8') as prediction:
            tag_lines = target.read().split('\n')
            pred_lines = prediction.read().split('\n')

            count = 0.0
            match = 0.0
            for tags, preds in zip(tag_lines, pred_lines):
                if not OS:
                    tag = list(tags)
                    pred = list(preds)
                else:
                    tag = tags.split(' ')
                    pred = preds.split(' ')

                for t, p in zip(tag, pred):
                    if t == p:
                        match += 1
                    count += 1

    print("ACCURACY: {}".format(100.0 * (match / count)))
    return


def F1_Score(target_file, prediction_file, OS=True):
    """
    :param target_file: Name of the target file
    :param prediction_file: Name of the prediction file
    :param OS: Default True, whether to compare OS or Char
    :return: Prints Precision, Recall, F1 Score
    """
    with open(target_file, 'r', encoding='utf-8') as target:
        with open(prediction_file, 'r', encoding='utf-8') as prediction:
            tag_lines = target.read().split('\n')
            pred_lines = prediction.read().split('\n')

            tp = 0.0
            fp = 0.0
            fn = 0.0
            count = 0.0

            for tags, preds in zip(tag_lines, pred_lines):
                if not OS:
                    tag = list(tags)
                    pred = list(preds)
                else:
                    tag = tags.split(' ')
                    pred = preds.split(' ')

                tag = set(tag)
                pred = set(pred)

                trueP = len(tag & pred)
                falseP = len(pred) - trueP
                falseN = len(tag) - trueP
                count += max(len(tag), len(pred))

        tp += trueP
        fp += falseP
        fn += falseN

    if tp > 0:
        precision = float(tp) / (tp + fp)
        recall = float(tp) / (tp + fn)
        f1_score = (2 * ((precision * recall) / (precision + recall))) / count
        print("PRECISION: {}, RECALL: {}, F1_SCORE: {}".format(precision, recall, f1_score))
        return
    return


def main(args):
    if args[1] == 'acc':
        accuracy(args[2], args[3], args[4])
    else:
        F1_Score(args[2], args[3], args[4])
    return


if __name__ == "__main__":
    sys.exit(main(sys.argv))
