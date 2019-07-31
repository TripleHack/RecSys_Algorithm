#-*-coding:utf-8-*-
"""
author:TripleHack
date:20190425
Content Based reader
"""
import os
import operator

def get_ave_score(input_file):
    if not os.path.exists(input_file):
        return {}
    record = {}
    ave_score = {}
    fp = open(input_file)
    for line in fp:
        item = line.strip().split("::")
        userid, itemid, rating = item[0], item[1], float(item[2])
        if itemid not in record:
            record[itemid] = [0, 0]
        record[itemid][0] += 1
        record[itemid][1] += rating
    fp.close()
    for itemid in record:
        ave_score[itemid] = round(record[itemid][1] / record[itemid][0], 3)
    return ave_score

def get_item_cate(ave_score, input_file):
    """
    Args:
        ave_score: a dict, key itemid value rating score
        input_file: item info file
    Return:
        a dict: key itemid value a dict, key: cate value: ratio
        a dict: key cate value[itemid1, itemid2, itemid3]
    """
    if not os.path.exists(input_file):
        return {},{}
    topk = 100
    item_cate = {}
    record = {}
    cate_sorted = {}
    fp = open(input_file, encoding = 'latin1')
    for line in fp:
        item = line.strip().split("::")
        itemid = item[0]
        cate_list = item[2].strip().split("|")
        ratio = round(1/len(cate_list), 3)
        if itemid not in item_cate:
            item_cate[itemid] = {}
        for fixed_cate in cate_list:
            item_cate[itemid][fixed_cate] = ratio
    fp.close()
    for itemid in item_cate:
        for cate in item_cate[itemid]:
            if cate not in record:
                record[cate] = {}
            itemid_rating = ave_score.get(itemid, 0)
            record[cate][itemid] = itemid_rating
    for cate in record:
        if cate not in cate_sorted:
            cate_sorted[cate] = []
        for tuple in sorted(record[cate].items(), key = operator.itemgetter(1), reverse = True)[:topk]:
            cate_sorted[cate].append(tuple[0])
    return item_cate, cate_sorted


if __name__ == "__main__":
    ave_score = get_ave_score("../data/ratings.dat")
    # print(len(ave_score))
    # print(ave_score["31"])

    item_cate, cate_sorted = get_item_cate(ave_score, "../data/movies.dat")
    print(cate_sorted)

    # fp = open("../data/ratings.dat")
    # min = 1000000000
    # for line in fp:
    #     item = line.strip().split("::")
    #     timestamp = int(item[3])
    #     if timestamp < min:
    #         min = timestamp
    # fp.close()
    # print(min)