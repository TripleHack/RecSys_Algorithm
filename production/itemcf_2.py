#-*-coding:utf-8-*-
"""
item cf v2
author:TripleHack
date:20190422
"""
import sys
sys.path.append("../util")
import util.reader as reader
import math
import operator



def contribute_score(click_num):
    return 1/math.log10(1 + click_num)

def cal_item_sim(user_click):
    item_user_click_time = {}
    co_appear = {}
    item_sim_score = {}
    for userid, itemlist in user_click.items():
        for index_i in range(0, len(itemlist)):
            item_i = itemlist[index_i]
            item_user_click_time.setdefault(item_i, 0)
            item_user_click_time[item_i] += 1
            for index_j in range(index_i, len(itemlist)):
                item_j = itemlist[index_j]
                co_appear.setdefault(item_i, {})
                co_appear[item_i].setdefault(item_j, 0)
                co_appear[item_i][item_j] += contribute_score(len(itemlist))

                co_appear.setdefault(item_j, {})
                co_appear[item_j].setdefault(item_i, 0)
                co_appear[item_j][item_i] += contribute_score(len(itemlist))

    for item_i, values in co_appear.items():
        for item_j, co_time in values.items():
            sim_score = co_time/math.sqrt(item_user_click_time[item_i] * item_user_click_time[item_j])
            item_sim_score.setdefault(item_i, {})
            item_sim_score[item_i].setdefault(item_j, 0)
            item_sim_score[item_i][item_j] = sim_score

    for itemid in item_sim_score:
        # sorted过后将不再是dict，而是list
        item_sim_score[itemid] = sorted(item_sim_score[itemid].items(), key = operator.itemgetter(1), reverse = True)

    return item_sim_score

def cal_recom_result(item_sim, user_click):
    recent_click_num = 5
    topk = 5
    recom_info = {}
    for userid in user_click:
        recom_info.setdefault(userid, {})
        for itemid in user_click[userid][:recent_click_num]:
            if itemid not in item_sim:
                continue
            for items in item_sim[itemid][:topk]:
                item_sim_id = items[0]
                item_sim_score = items[1]
                recom_info[userid][itemid] = item_sim_score
    return recom_info

def debug_recomresult(recom_result, item_info):
    user_id = "1"
    if user_id not in recom_result:
        print("invalid result")
        return
    for zuhe in sorted(recom_result[user_id].items(), key = operator.itemgetter(1), reverse = True):
        itemid, score = zuhe
        if itemid not in item_info:
            continue
        print(",".join(item_info[itemid]) + "\t" + str(score))

def debug_itemsim(item_info, sim_info):
    fixed_itemid = "1"
    if fixed_itemid not in item_info:
        print("invalid itemid")
        return
    [fixed_title, fixed_genres] = item_info[fixed_itemid]
    for tuple in sim_info[fixed_itemid][:6]:
        itemid_sim, score_sim = tuple
        if itemid_sim not in item_info:
            continue
        if fixed_itemid == itemid_sim:
            continue
        [title, genres] = item_info[itemid_sim]
        print(fixed_title + "\t" + fixed_genres + "\tsim:" + title + "\t" + genres + "\t" + str(score_sim))


def main_flow():
    user_click = reader.get_user_click("../data/ratings.dat")
    item_info = reader.get_item_info("../data/movies.dat")
    sim_info = cal_item_sim(user_click)
    recom_result = cal_recom_result(sim_info, user_click)

    # debug_recomresult(recom_result, item_info)
    debug_itemsim(item_info, sim_info)


if __name__ == "__main__":
    main_flow()
