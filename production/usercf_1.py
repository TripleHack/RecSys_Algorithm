#-*-coding:utf-8-*-
"""
basic user cf
author:TripleHack
date:20190422
"""
import sys
sys.path.append("../util")
import util.reader_2 as reader
import operator
import math

def transfer_user_click(user_click):
    item_click = {}
    for user in user_click:
        for itemid in user_click[user]:
            item_click.setdefault(itemid, [])
            item_click[itemid].append(user)
    return item_click

def contribution_score():
    return 1

def cal_user_sim(item_click):
    co_appear = {}
    user_click_count = {}
    user_sim = {}
    for itemid, user_list in item_click.items():
        for index_i in range(0, len(user_list)):
            user_i = user_list[index_i]
            user_click_count.setdefault(user_i, 0)
            user_click_count[user_i] += 1
            for index_j in range(index_i + 1, len(user_list)):
                user_j = user_list[index_j]
                co_appear.setdefault(user_i, {})
                co_appear[user_i].setdefault(user_j, 0)
                co_appear[user_i][user_j] += contribution_score()

                co_appear.setdefault(user_j, {})
                co_appear[user_j].setdefault(user_i, 0)
                co_appear[user_j][user_i] += contribution_score()
    for user_i, related_user in co_appear.items():
        user_sim.setdefault(user_i, {})
        for user_j,cotime in related_user.items():
            user_sim[user_i].setdefault(user_j, 0)
            user_sim[user_i][user_j] = cotime / math.sqrt(user_click_count[user_i] * user_click_count[user_j])
    for user in user_sim:
        user_sim[user] = sorted(user_sim[user].items(), key = operator.itemgetter(1), reverse = True)
    return user_sim

def cal_recom_result(user_click, user_sim):
    recom_result = {}
    for user, item_list in user_click.items():
        tmp_dict = {}
        for itemid in item_list:
            tmp_dict.setdefault(itemid, 1)
        recom_result.setdefault(user, {})
        for tuple in user_sim[user][:6]:
            related_user,sim_score = tuple
            if related_user not in user_click:
                continue
            if related_user == user:
                continue
            for related_item in user_click[related_user][:6]:
                if related_item in tmp_dict:
                    continue
                recom_result[user].setdefault(related_item, sim_score)
    return recom_result



def main_flow():
    user_click, user_click_time = reader.get_user_click("../data/ratings.dat")
    item_click = transfer_user_click(user_click)
    user_sim = cal_user_sim(item_click)
    recom_result = cal_recom_result(user_click, user_sim)
    print(recom_result["1"])

if __name__ == "__main__":
    main_flow()