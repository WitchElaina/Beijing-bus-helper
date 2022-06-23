"""
select best route from all_path list by user's preference
"""
import st_praser 
import search

def min_change(all_path: list):
    """
    返回换乘次数最少的路径, 如有平行方案全部输出, 所有结果存储在列表中
    eg. [[best1], [best2]] or [[best]]
    get minimum change_line route
    :param all_path: 所有备选路径 all routes in list
    :return: 最优方案列表 best route(s) in list
    """
    ret = []
    counts = []
    for content in all_path:
        counts.append(search.cal_change_time(content))
    for i in all_path:
        if counts[all_path.index(i)] == min(counts):
            ret.append(i)
    return ret


def min_station(all_path: list):
    """
    返回经过站点最少的路径, 如有平行方案全部输出, 所有结果存储在列表中
    eg. [[best1], [best2]] or [[best]]
    get minimum change_line route
    :param all_path: 所有备选路径 all routes in list
    :return: 最优方案列表 best route(s) in list
    """
    ret = []
    counts = []
    for content in all_path:
        counts.append(len(content))
    for content in all_path:
        if len(content) == min(counts):
            ret.append(content)

    return ret
