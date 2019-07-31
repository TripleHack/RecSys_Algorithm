#-*-coding:utf-8-*-
"""
author:TripleHack
date:20190423
mat util for personal rank algo
"""
from scipy.sparse import coo_matrix
import numpy as np
import util.read as read
def graph_to_m(graph):
    """
    Args:
        graph: user item graph
    Return:
        coo_matrix, sparse mat M
        list, total user item point
        dict, map the point to row index
    """
    vertex = list(graph.keys())
    address_dict = {}
    total_len = len(vertex)
    row = []
    col = []
    data = []
    for index in range(total_len):
        address_dict[vertex[index]] = index
    for ele_i in graph:
        weight = round(1 / len(graph[ele_i]), 3)
        row_index = address_dict[ele_i]
        for ele_j in graph[ele_i]:
            col_index = address_dict[ele_j]
            row.append(row_index)
            col.append(col_index)
            data.append(weight)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    matrix = coo_matrix((data, (row, col)), shape = (total_len, total_len))
    return matrix, vertex, address_dict


def mat_all_point(m_mat, vertex, alpha):
    """
    get E-alpha*m_mat.T
    Args:
        m_mat:
        vertex: total item and user point
        alpha: the prob for random walking
    Return:
        a sparse
    """
    total_len = len(vertex)
    row = []
    col = []
    data = []
    for index in range(total_len):
        row.append(index)
        col.append(index)
        data.append(1)
    row = np.array(row)
    col = np.array(col)
    data = np.array(data)
    eye_t = coo_matrix((data, (row, col)), shape = (total_len, total_len))
    return eye_t.tocsr() - alpha * m_mat.tocsr().transpose()


if __name__== "__main__":
    graph = read.get_graph_from_data("../data/log.txt")
    m, vertex, address_dict = graph_to_m(graph)
    # print(address_dict)
    # print(m.todense())
    # print(mat_all_point(m, vertex, 0.8))

