#-*-coding:utf-8-*-
"""
user cf v3
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

def contribution_score(start, end):
    delta_time = abs(end - start)
    delta_time /= 60 * 60 *24
    return 1/(1 + delta_time)

def cal_user_sim(item_click, user_click_time):
    co_appear = {}
    user_click_count = {}
    user_sim = {}
    for itemid, user_list in item_click.items():
        for index_i in range(0, len(user_list)):
            user_i = user_list[index_i]
            user_click_count.setdefault(user_i, 0)
            user_click_count[user_i] += 1
            if user_i + "_" + itemid not in user_click_time:
                click_time_start = 0
            else:
                click_time_start = user_click_time[user_i + "_" + itemid]
            for index_j in range(index_i + 1, len(user_list)):
                user_j = user_list[index_j]
                if user_j + "_" + itemid not in user_click_time:
                    click_time_end = 0
                else:
                    click_time_end = user_click_time[user_j + "_" + itemid]
                co_appear.setdefault(user_i, {})
                co_appear[user_i].setdefault(user_j, 0)
                co_appear[user_i][user_j] += contribution_score(click_time_start, click_time_end)

                co_appear.setdefault(user_j, {})
                co_appear[user_j].setdefault(user_i, 0)
                co_appear[user_j][user_i] += contribution_score(click_time_start, click_time_end)
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

def debug_user_sim(user_sim):
    fixed_user = "1"
    if fixed_user not in user_sim:
        print("invalid user")
        return
    for tuple in user_sim[fixed_user][:6]:
        userid, score = tuple
        print(fixed_user + "\tsim_user_" + userid + "\t" + str(score))

def debug_recom_result(item_info, recom_result):
    fixed_user = "1"
    if fixed_user not in recom_result:
        print("invalid user")
        return
    for itemid in recom_result[fixed_user]:
        if itemid not in item_info:
            continue
        recom_score = recom_result[fixed_user][itemid]
        print("recom_result:" + ",".join(item_info[itemid]) + "\t" + str(recom_score))




def main_flow():
    user_click, user_click_time = reader.get_user_click("../data/ratings.dat")
    item_info = reader.get_item_info("../data/movies.dat")
    item_click = transfer_user_click(user_click)
    user_sim = cal_user_sim(item_click, user_click_time)

    debug_user_sim(user_sim)

    # recom_result = cal_recom_result(user_click, user_sim)
    # debug_recom_result(item_info,recom_result)


if __name__ == "__main__":
    main_flow()