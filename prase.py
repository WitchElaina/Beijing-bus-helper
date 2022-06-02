"""
prase.py
用于从st.txt文档中提取站点信息, 并将其转化为python对象
"""

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
    :return: 包含所有线路信息的字典
    """
    content = []
    f1 = open(filename, 'rt', encoding="utf-8")
    for line in f1:
        value = line[line.index('[')+2:-3].split("', '")
        content.extend(value)
    f1.close()
    content = list(set(content))
    return content


def to_adj_list():
    """
    convert txt to adjacency list
    :return: a dict like {vertex:[adj, adj, ...], ...}
    """
    # TODO
    pass
