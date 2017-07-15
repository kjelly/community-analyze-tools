#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             'jieba-zh_TW'))

import json
import re
import jieba
from collections import defaultdict
import base64
import operator


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def safe_file_name(name):
    name = name.replace(' ', '_')
    name = name.replace('/', '_')
    return name


SCHEMA = '''
[u'groups']
[u'name', u'links', u'events']
[u'url', u'start_datetime', u'name', u'description']

'''

def main():
    if not os.path.exists('./output'):
        os.mkdir('./output')
    with open('./groups.json', 'r') as ftr:
        data = json.loads(ftr.read())

    all_word_map = defaultdict(int)

    for i in data['groups']:
        word_map = defaultdict(int)
        for j in i['events']:
            description = cleanhtml(j['description'])
            words = jieba.cut(description)
            for k in words:
                word_map[k] += 1
                all_word_map[k] += 1
        if len(word_map) == 0:
            continue
        with open('output/' + safe_file_name(i['name']) + '.json', 'w') as ftr:
            ftr.write(json.dumps(word_map, ensure_ascii=False))

        sorted_x = sorted(word_map.items(), key=operator.itemgetter(1))
        with open('output/' + safe_file_name(i['name']) + '.txt', 'w') as ftr:
            for j in sorted_x:
                ftr.write('%s: %s\n' % (j[0], j[1]))

    with open('output/total.json', 'w') as ftr:
        ftr.write(json.dumps(all_word_map, ensure_ascii=False))

    sorted_x = sorted(all_word_map.items(), key=operator.itemgetter(1))
    with open('output/total.txt', 'w') as ftr:
        for j in sorted_x:
            ftr.write('%s: %s\n' % (j[0], j[1]))

if __name__ == '__main__':
    main()
