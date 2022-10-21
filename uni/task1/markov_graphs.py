#  Copyright (c) Evgeniya Zemlyanaya @zzemlyanaya 21/10/2022

import re

with open('idiot.txt') as f1:
    with open('igrok.txt') as f2:
        words = re.findall(r'[\w]+', f1.read()) + re.findall(r'[\w]+', f2.read())
        freq = dict()

        for x in words:
            if x in freq.keys():
                freq[x][0] += 1
            else:
                freq[x] = [1, 0.0]

        count = len(words)
        for x in freq.keys():
            freq[x][1] = freq[x][0] / count

        freq = dict(sorted(freq.items(), key=lambda item: item[1][0], reverse=True))

        for k, v in freq.items():
            print(k, *v)