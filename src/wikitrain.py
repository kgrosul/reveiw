import wikipedia
from .train import file_train
from .train import normalize
import argparse
import pickle
import collections


def wiki_train(model_file, texts_num, words_num, lowercase=False):
    """

    Функция строит модель используя texts_num(количество) случайно
    найденных в Википедии текстом. Для доступа к Википедии используется
    модуль wikipedia.

    wiki_train(model_file, texts_num, words_num, lowercase=False)

    model_file: файл для хранения модели
    texts_num: количество текстов
    words_num: количество слов, на основании которых
                    выбирается следующее
    lowercase: приводить ли к lowercase, default = False

    """

    file = open(model_file, 'w')
    for i in range(texts_num):
        file.write(wikipedia.page(wikipedia.search(
            wikipedia.random())[-1]).content)

    file.close()
    model_dict = collections.defaultdict(
        lambda: collections.defaultdict(int))

    file_train(model_dict, model_file, words_num, lowercase)
    normalize(model_dict)

    with open(model_file, 'wb') as output:
        pickle.dump(dict(model_dict), output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Build model for generate.py using random texts "
                    "from Wikipedia. You can set model file name, number "
                    "of texts,n in n-gramm and should the text be lowercase "
                    "or not"
    )

    required = parser.add_argument_group('required arguments')

    parser.add_argument("--texts-num",
                        type=int,
                        default=1,
                        help="number of texts from Wikipedia"
                        )

    required.add_argument("--model",
                          type=str,
                          help="path to to the model file",
                          required=True
                          )

    parser.add_argument("--lc",
                        action='store_true',
                        default=False,
                        help="converting text to the lower case"
                        )

    parser.add_argument("--words-num",
                        type=int,
                        default=1,
                        help="length of a Markov chain"
                        )

    args = parser.parse_args()
    wiki_train(args.model, args.texts_num, args.words_num, args.lc)
