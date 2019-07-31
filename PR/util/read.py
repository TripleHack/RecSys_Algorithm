#-*-coding:utf8-*-
"""
author:TripleHack
date:20190423
get graph from user data
"""
import os

def get_graph_from_data(input_file):
    """
    Args:
        input_file: user item rating file
    Return:
        a dict: {UserA:{itemb:1, itemc:1}, itemb:{UserA:1}}
    """
    if not os.path.exists(input_file):
        return {}
    graph = {}
    score_thr = 4.0
    fp = open(input_file)
    for line in fp:
        item = line.strip().split("::")
        userid, itemid, rating = item[0], "item_" + item[1], item[2]
        if float(rating) < score_thr:
            continue
        if userid not in graph:
            graph[userid] = {}
        graph[userid][itemid] = 1
        if itemid not in graph:
            graph[itemid] = {}
        graph[itemid][userid] = 1
    fp.close()
    return graph

def get_item_info(input_file):
    """
    get item info:[title,genre]
    Args:
        input_file:item info file
    Return:
         a dict: key itemid, value:[title, genre]
    """

    if not os.path.exists(input_file):
        return {}
    item_info = {}
    fp = open(input_file,'r',encoding='ISO-8859-1')
    for line in fp:
        item = line.strip().split('::')
        itemid, title, genre = item[0], item[1], item[2]
        item_info[itemid] = [title, genre]
    fp.close()
    return item_info


if __name__ =="__main__":
    graph = get_graph_from_data("../data/ratings.dat")
    print(graph)