#-*-coding:utf-8-*-
"""
author:TripleHack
date:20190418
"""
import os

def get_user_click(rating_file):
    if not os.path.exists(rating_file):
        return {}
    fp = open(rating_file)
    user_click = {}
    for line in fp:
        item = line.strip().split("::")
        userid, itemid, rating, timestamp = item[0], item[1], item[2], item[3]
        if float(rating) < 4.0:
            continue
        if userid not in user_click:
            user_click[userid] = []
        user_click[userid].append(itemid)
    fp.close()
    return user_click

def get_item_info(item_file):
    if not os.path.exists(item_file):
        return {}
    fp = open(item_file, encoding = 'latin1')
    item_info = {}
    for line in fp:
        item = line.strip().split("::")
        itemid, title, genres = item[0], item[1], item[2]
        if itemid not in item_info:
            item_info[itemid] = {}
        item_info[itemid] = [title,genres]
    fp.close()
    return item_info




if __name__ == "__main__":
    user_click = get_user_click("../data/ratings.dat")
    item_info = get_item_info("../data/movies.dat")
    print(user_click["1"])
    print(item_info["18"])


