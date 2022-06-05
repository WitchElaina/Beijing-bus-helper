"""
search routes between two stations
"""
import st_praser as sp
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
    graph = sp.to_adj_list()
    dfs_search_all(st, ed, graph)
    print(all_path)
