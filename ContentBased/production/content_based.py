#-*-coding:utf-8-*-
"""
author:TripleHack
date:20190425
get up an online recommendation
"""
import os
import operator
import sys
sys.path.append("../")
import util.read as read

def get_up(item_cate, input_file):
    """
    Args:
        item_cate: key itemid, value: dict, key category value ratio
        input_file: user rating file
    Return:
        a dict: key userid, value[(category, ratio),(category1, ratio1)]
    """
    if not os.path.exists(input_file):
        return {}
    score_thr = 4.0
    record = {}
    up = {}
    fp = open(input_file)
    for line in fp:
        item = line.strip().split("::")
        userid, itemid, rating, timestamp = item[0], item[1], float(item[2]), item[3]
        if rating < score_thr:
            continue
        if itemid not in item_cate:
            continue
        time_score = get_time_score(timestamp)
        if userid not in record:
            record[userid] = {}
        for fixed_cate in item_cate[itemid]:
            if fixed_cate not in record[userid]:
                record[userid][fixed_cate] = 0
            record[userid][fixed_cate] += rating * time_score * item_cate[itemid][fixed_cate]
    fp.close()


    topk = 2
    for userid in record:
        if userid not in up:
            up[userid] = []
        total_score = 0
        for tuple in sorted(record[userid].items(), key = operator.itemgetter(1), reverse = True)[:topk]:
            up[userid].append((tuple[0], tuple[1]))
            total_score += tuple[1]
        for index in range(len(up[userid])):
            up[userid][index] = (up[userid][index][0], round(up[userid][index][1] / total_score, 3))
    return up

def get_time_score(timestamp):
    """
    Args:
        timestamp(max = 1046454590, min = 956703932)
    Return:
        time score
    """
    fixed_time_stamp = 1046454590
    delta = (fixed_time_stamp - int(timestamp)) / (24 * 60 * 60 * 100)
    return round(1/(1+delta), 3)


def recom(cate_sorted, up, userid, topk = 10):
    """
    Args:
        cate_sorted: reverse sort cate
        up: user profile
        userid: fixed user
        topk: recom num
    Return:
        a dict, key userid value [itemid1, itemid2]
    """
    if userid not in up:
        return {}
    result = {}
    if userid not in result:
        result[userid] = []
    for tuple in up[userid]:
        cate = tuple[0]
        ratio = tuple[1]
        num = int(topk * ratio) + 1
        if cate not in cate_sorted:
            continue
        recom_list = cate_sorted[cate][:num]
        result[userid] += recom_list
    return result

def run_main():
    ave_score = read.get_ave_score("../data/ratings.dat")
    item_cate, cate_sorted = read.get_item_cate(ave_score, "../data/movies.dat")
    up = get_up(item_cate, "../data/ratings.dat")
    print(up["1"])
    print(recom(cate_sorted, up, "1", ))

if __name__ == "__main__":
    run_main()


