#  Copyright (c) Evgeniya Zemlyanaya @zzemlyanaya 14/10/2022

import re

with open('idiot.txt') as f1:
    with open('igrok.txt') as f2:
        words = re.findall(r'[\w]+', f1.read()) + re.findall(r'[\w]+', f2.read())
        # count = len(words)
        answer = dict()

        for x in words:
            if x in answer.keys():
                answer[x] += 1
            else:
                answer[x] = 1

        answer = dict(sorted(answer.items(), key=lambda item: item[1], reverse=True))

        for k, v in answer.items():
            print(k, v)
