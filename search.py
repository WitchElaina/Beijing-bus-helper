"""
search routes between two stations
"""
import st_praser as sp
import route_suggest
import sys

sys.setrecursionlimit(10000000)


def is_change(path):
    """
    check if a path contains multi lines
    :param path: stations on path, List of station name str
    :return: bool
    """
    if len(path) <= 2:
        return False

    # reverse path
    path_rev = set(path[::-1])
    or_path = set(path)

    all_line = sp.to_dict()
    for i in all_line.values():
        i = set(i)
        if or_path.issubset(i) or path_rev.issubset(i):
            return False
    return True


def cal_change_time(path:list):    
    """
    单路径的换乘数计算
    结果存在counts中
    """
    List_1 = []
    lineList_2 = []
    lineList_1 = []
    lineList = []
    text = sp.to_dict()
    left = 0
    right = 1
    while right < len(path):
        for key in text:
            if path[left] in text[key] and path[left+1] in text[key] :
                    List_1.append(key)
        while len(List_1) > 0 and right < len(path) :
            for f1 in List_1:
                lineList_1 = []
                if path[right] in text[f1] :
                    List_1 = []
                    List_1.append(f1)
                    lineList_1.append(f1)
                    break
                if path[right] not in text[f1] :
                    lineList_2.append(f1) 
                    continue
            if len(lineList_1) == 0:
                lineList.append(lineList_2[0])
                List_1 = []
                lineList_2 = []
                left = right - 1
                if right == len(path) - 1:
                    right = right - 1
            if right == len(path) - 1 and len(List_1) != 0:
                lineList.append(List_1[0])
                List_1 = []
                lineList_2 = []
            right = right + 1
    counts = len(lineList) - 1
    lineList = []
    return counts


def pruning(path):
    """
    puring func for DFS, calculate the number of lines in path
    :param path: stations in str list
    :return: number of lines
    """
    req = []
    change_num = 0
    for i in path:
        req.append(i)
        if is_change(req):
            change_num += 1
            req = [i]
    return change_num


path = []
all_path = []
run_info = 0


def dfs_search_all(st, ed, graph):
    """
    DFS search all routes from st to ed, if a path contains too many (default: 3) lines, abandon search this route
    :param st: start station
    :param ed: destination station
    :param graph: graph in adjacency list
    :return: all routes in list
    """
    global path, all_path, run_info
    path.append(st)
    run_info += 1
    # check
    if st == ed:
        all_path.append(path.copy())
        # print(all_path[-1])
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
    st, ed = '北京航空航天大学', '北京西站'
    graph = sp.to_adj_list()
    dfs_search_all(st, ed, graph)
    # print(cal_change_time(all_path[0]))
