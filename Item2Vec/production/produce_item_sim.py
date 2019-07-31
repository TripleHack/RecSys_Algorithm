#-*-coding:utf-8-*-
"""
author:TripleHack
date:20190425
produce item sim file
"""
import os
import numpy as np
import operator
def load_item_vec(input_file):
    """
    Args:
        input_file: item vec file
    Return:
        dict: key:itemid value:np.array[num1, num2...]
    """
    if not os.path.exists(input_file):
        return {}
    fp = open(input_file)
    linenum = 0
    item_vec = {}
    for line in fp:
        if linenum ==0:
            linenum += 1
            continue
        item = line.strip().split()
        if len(item) < 129:
            continue
        itemid = item[0]
        if itemid == "</s>":
            continue
        item_vec[itemid] = np.array([float(ele) for ele in item[1:]])
    fp.close()
    return item_vec

def cal_item_sim(item_vec, itemid, output_file):
    """
    Args:
        item_vec: item embedding vector
        itemid: itemid to clac item sim
        output_file: the file to store result
    """
    if itemid not in item_vec:
        return
    fixed_itemvec = item_vec[itemid]
    score = {}
    topk = 10
    for tmp_itemid in item_vec:
        if tmp_itemid == itemid:
            continue
        tmp_itemvec = item_vec[tmp_itemid]
        denominator = np.linalg.norm(fixed_itemvec)*np.linalg.norm(tmp_itemvec)
        if denominator == 0:
            score[tmp_itemid] = 0
        else:
            score[tmp_itemid] = round(np.dot(fixed_itemvec,tmp_itemvec)/denominator, 3)
    fw = open(output_file, "w+")
    out_str = itemid + "\t"
    tmp_list = []
    for tuple in sorted(score.items(), key = operator.itemgetter(1), reverse = True)[:topk]:
        tmp_list.append("item:" + tuple[0] + "_score:" + str(tuple[1]))
    out_str += ";".join(tmp_list)
    fw.write(out_str + "\n")
    fw.close()

def run_main(input_file, output_file):
    item_vec = load_item_vec(input_file)
    cal_item_sim(item_vec, "260", output_file)







if __name__ == "__main__":
    # item_vec = load_item_vec("../data/item_vec.txt")
    # print(len(item_vec))
    # print(item_vec["260"])

    run_main("../data/item_vec.txt", "../data/sim_result.txt")