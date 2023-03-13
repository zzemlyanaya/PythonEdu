#  Copyright (c) Evgeniya Zemlyanaya @zzemlyanaya 21/10/2022

import re
import numpy as np


def make_pairs(words):
    for word in range(len(words) - 1):
        yield words[word], words[word + 1]


with open('idiot.txt') as f1:
    with open('igrok.txt') as f2:
        words = re.findall(r'[\w]+', f1.read()) + re.findall(r'[\w]+', f2.read())
        pairs = make_pairs(words)
        word_dict = {}
        for word_1, word_2 in pairs:
            if word_1 in word_dict.keys():
                word_dict[word_1].append(word_2)
            else:
                word_dict[word_1] = [word_2]

        first_word = np.random.choice(words)

        while first_word.islower():
            chain = [first_word]
            n_words = 20
            first_word = np.random.choice(words)

            for i in range(n_words):
                chain.append(np.random.choice(word_dict[chain[-1]]))

        print(' '.join(chain))
