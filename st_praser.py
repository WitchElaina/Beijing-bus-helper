"""
st_praser.py
用于从st.txt文档中提取站点信息, 并将其转化为python对象
"""
import multiprocessing as mp
filename = ''


def load(f_name: str):
    """
    初始化函数, 设置数据源的路径和文件名
    :param f_name: 数据源文件名
    :return: None
    """
    global filename
    filename = f_name


def to_dict():
    """
    将txt转化为字典并输出, 键为线路名称, 值为线路站点列表
    :return: 包含所有线路信息的字典
    """
    content = {}
    f1 = open(filename, 'rt', encoding="utf-8")
    for line in f1:
        key = line[:line.index('-')]
        value = line[line.index('[')+2:-3].split("', '")
        content[key] = value
    f1.close()
    return content


def to_list():
    """
    将txt中所有站点存放在列表中, 返回一个包含所有站点且无重复站点的列表
    :return: 包含所有线路信息的列表
    """
    content = []
    f1 = open(filename, 'rt', encoding="utf-8")
    for line in f1:
        value = line[line.index('[')+2:-3].split("', '")
        content.extend(value)
    f1.close()
    content = list(set(content))
    return content


def get_adj(st, adj_list):
    """
    get all adjacency station for st
    :param st: station
    :return: list of station's adjacency
    """
    load('st.txt')
    ret = []
    all_stations = to_dict().values()
    for line in all_stations:
        if st in line:
            loc = line.index(st)
            if loc == 0:
                if line[1] not in ret:
                    ret.append(line[1])
            elif loc == len(line)-1:
                if line[len(line)-2] not in ret:
                    ret.append(line[len(line)-2])
            else:
                if line[loc-1] not in ret:
                    ret.append(line[loc-1])
                if line[loc+1] not in ret:
                    ret.append(line[loc+1])
    adj_list[st] = ret


def get_dfs_adj(st, adj_list):
    """
    get all dfs_search adjacency station for st
    :param st: station
    :return: dict of st's adjacency
    """
    load('st.txt')
    # print(st)
    ret = []
    all_stations = to_dict().values()
    for line in all_stations:
        if st in line:
            loc = line.index(st)
            if loc == 0:
                if line[1] not in ret:
                    ret.append(line[1])
            elif loc == len(line)-1:
                if line[len(line)-2] not in ret:
                    ret.append(line[len(line)-2])
            else:
                if line[loc-1] not in ret:
                    ret.append(line[loc-1])
                if line[loc+1] not in ret:
                    ret.append(line[loc+1])
    # print(st, end='->')
    # print(ret)
    ret_dict = {}
    for i in ret:
        ret_dict[i] = False
    adj_list[st] = ret_dict


def to_adj_list():
    """
    convert txt to adjacency list, use multiprocessing to improve performance
    :return: a dict like {vertex:[adj, adj, ...], ...}
    """
    # all stations
    st_list = to_list()

    # create processing pool by cpu core counts
    pool = mp.Pool(mp.cpu_count())

    # creat shared dict to store data
    adj_list = mp.Manager().dict()

    # push process to pool
    for st in st_list:
        pool.apply_async(get_adj, args=(st, adj_list))
    pool.close()
    pool.join()
    return adj_list


def to_dfs_adj_list():
    """
    convert txt to dfs_search adjacency list, use multiprocessing to improve performance
    :return: a dict like {vertex:[adj: is_visited, adj: is_visited, ...], ...}
    """
    # all stations
    st_list = to_list()

    # create processing pool by cpu core counts
    pool = mp.Pool(mp.cpu_count())

    # creat shared dict to store data
    adj_list = mp.Manager().dict()

    # push process to pool
    for st in st_list:
        pool.apply_async(get_dfs_adj, args=(st, adj_list))
    pool.close()
    pool.join()
    return adj_list


# if __name__ == '__main__':
#     load('st.txt')
#     # print('Loading...', end=str(len(to_list())))
#     adj_list = to_adj_list()
#     print(adj_list['北京科技大学北门'])
#     print(len(adj_list))
