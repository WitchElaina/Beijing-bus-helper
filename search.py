"""
search ret between two stations, contains multi algorithm like BFS, DFS, etc.
"""
import copy
from collections import deque
from operator import contains

import st_praser as sp
import os
import sys

sys.setrecursionlimit(10000000)


def bfs_search(st, ed):
    search_queue = deque()
    search_queue.append(st)
    path = {}
    ret = []
    visited = []
    graph = copy.deepcopy(sp.to_adj_list())
    while search_queue:
        check_point = search_queue.pop()
        visited.append(check_point)
        if check_point == ed:
            # finded
            st_node = check_point
            while True:
                ret.append(st_node)
                if st_node == st:
                    return ret
                st_node = path[st_node]

        else:
            for i in graph[check_point]:
                if not (i in visited):
                    search_queue.append(i)
                    path[i] = check_point


def st_extend(st):
    """
    return other stations in the same line
    :param st: station
    :return: list of station
    """
    ret = []
    all_line = sp.to_dict()
    for line in all_line.keys():
        if st in all_line[line]:
            for i in all_line[line]:
                if i not in ret and i != st:
                    ret.append(i)
    return ret


def find_drct_des(st_list, ed):
    """
    judge if st and ed in the same line
    :param st_list: start station
    :param ed: end station
    :return: True or False
    """
    ret = {}

    for st in st_list:
        # init direct lines
        lines = {}

        # find all line pass by start station
        all_line = sp.to_dict()
        for line in all_line.keys():
            if st in all_line[line]:
                # insert to dict
                lines[line] = all_line[line]

        # check if ed in lines
        for line in lines.keys():
            if ed in lines[line]:
                # insert to ret dict
                ret[st] = line
    return ret


def min_change_search(st, ed, change_num=0, cur_route={}):
    """
    search minimum change line path from st to ed
    :param adj_list: road map in adj_list form
    :param st: start station
    :param ed: end station
    :param change_num: change times
    :return: paths
    """
    ex_st = st_extend(st)
    ret = find_drct_des(st, ed)
    # todo
    cur_route[st] = ret
    if ret == ed or change_num > 1:
        return cur_route
    else:
        return min_change_search(ex_st, ed, change_num + 1, cur_route)


def dfs_search(st, ed):
    graph = copy.deepcopy(sp.to_dfs_adj_list())
    stack = []
    path = []
    stack.append(st)
    while stack:
        father = stack.pop()

        if father == ed:
            # finded
            path.append(father)
            return path
        else:
            # find a unvisited node
            unvisited = None
            for station in graph[father].keys():
                if not graph[father][station]:
                    unvisited = station
                    graph[father][station] = True
                    # print(graph[father])
                    break
            if unvisited is not None:
                stack.append(unvisited)
                path.append(father)
            else:
                stack.append(path.pop())
    return False


def is_change(path):
    if len(path) <= 2:
        return False

    # reverse path
    path_rev = set(path[::-1])
    or_path = set(path)

    all_line = sp.to_dict()
    for i in all_line.values():
        # print(i)
        i = set(i)
        if or_path.issubset(i) or path_rev.issubset(i):
            return False
    return True


def pruning(path):
    req = []
    change_num = 0
    for i in path:
        req.append(i)
        if is_change(req):
            change_num += 1
            # print(str(change_num), end='')
            # print(req)
            req = [i]
    return change_num


# def dfs_search_all(st, ed):
#     graph = copy.deepcopy(sp.to_dfs_adj_list())
#     for i in graph[ed].keys():
#         graph[ed][i] = True
#     stack = []
#     path = []
#     all_path = []
#     stack.append(st)
#     while stack:
#         father = stack.pop()
#         if father == ed:
#             # found
#             print(path+[father])
#             all_path.append(path+[father])
#             # # TODO: traceback
#             # stack = [st]
#             # path = []
#             stack.append(path.pop())
#
#         else:
#             # find a unvisited node
#             unvisited = None
#             for station in graph[father].keys():
#
#                 if not graph[father][station]:
#                     # pruning
#                     if pruning(path+[station]) <= 3:
#                         unvisited = station
#                         graph[father][station] = True
#                         graph[station][father] = True
#                         break
#             # cur = graph[father]
#             if unvisited is not None:
#                 stack.append(unvisited)
#                 path.append(father)
#             else:
#                 # if father == st:
#                 #     return all_path
#                 if not path:
#                     return 'no'
#                 stack.append(path.pop())
#     return all_path

path = []
all_path = []
run_info = 0


def adj_simplify(st, ed, graph):
    ret = {st: graph[st], ed: graph[ed]}

    for j in range(2):
        keys = ret.keys()
        for i in keys:
            ret[i] = graph[i]

    print(len(ret))
    return ret


def dfs_search_all(st, ed, graph):
    global path, all_path, run_info
    path.append(st)
    run_info += 1
    # check
    if st == ed:
        all_path.append(path.copy())
        print(all_path[-1])

    else:
        for i in graph[st]:
            if i not in path:
                if pruning(path + [i]) <= 2:
                    dfs_search_all(i, ed, graph)

    path.pop()


if __name__ == '__main__':
    sp.load('st.txt')

    # st = input('Start:')
    # ed = input('Destination:')
    st, ed = '成府路口南', '北京西站'
    # graph = adj_simplify(st, ed, sp.to_adj_list())
    graph = sp.to_adj_list()
    # print(len(result), end='routes:\n')
    # for i in result:
    #     print(i)
    dfs_search_all(st, ed, graph)
    print(all_path)

    # req = ['成府路口南', '北京航空航天大学', '学知桥南', '蓟门桥北', '蓟门桥南', '明光桥南', '西直门南', '阜成门北', '北京儿童医院', '北京西站']
    #
    # print(pruning(req))
    #
    # ret = ['成府路口南', '北京航空航天大学', '北医三院', '塔院', '花园路', '北太平桥西', '蓟门桥东', '明光桥北', '文慧桥北', '索家坟', '西直门南', '阜成门北', '北京儿童医院', '复兴门南', '北京西站']

    # print(len(ret))
