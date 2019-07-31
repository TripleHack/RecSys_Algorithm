#-*-coding:utf-8-*-
"""
author:TripleHack
date:20190424
produce train data for item2vec
"""
import os

def produce_train_data(input_file, output_file):
    record = {}
    score_thr = 4.0
    fp = open(input_file)
    for line in fp:
        item = line.strip().split("::")
        user, item, score = item[0], item[1], float(item[2])
        if score < score_thr:
            continue
        if user not in record:
            record[user] = []
        record[user].append(item)
    fp.close()
    fw = open(output_file, 'w+')
    for user in record:
        fw.write(" ".join(record[user]) + "\n")
    fw.close()

if __name__ == '__main__':
    produce_train_data("../data/ratings.dat", "../data/train_data.txt")
