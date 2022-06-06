"""
select best route from all_path list by user's preference
"""
import st_praser 

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
    List_1 = []
    lineList_2 = []
    lineList_1 = []
    lineList = []
    text = st_praser.to_dict()
    for content in all_path:
        left = 0
        right = 2
        if len(content) == 2:
            ret.append(content)
            return ret
        while right < len(content):
            for key in text:
                if content[left] in text[key] and content[left+1] in text[key] :
                        List_1.append(key)
            while len(List_1) > 0 and right < len(content) :
                for f1 in List_1:
                    lineList_1 = []
                    if content[right] in text[f1] :
                        List_1 = []
                        List_1.append(f1)
                        lineList_1.append(f1)
                        break
                    if content[right] not in text[f1] :
                        lineList_2.append(f1) 
                        continue
                if len(lineList_1) == 0:
                    left = right - 1
                    lineList.append(lineList_2[0])
                    List_1 = []
                    lineList_2 = []
                    if right == len(content) - 1:
                        right = right - 1
                if right == len(content) - 1 and len(List_1) != 0:
                    lineList.append(List_1[0])
                    List_1 = []
                    lineList_2 = []
                right = right + 1
        counts.append(len(lineList) - 1)
        lineList = []
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
