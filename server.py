"""
bus helper command line client
"""

import search
import route_suggest
import st_praser

from flask import Flask
from flask_cors import CORS
from flask import request
import time

st = ""
ed = ""
adj_list = {}   # 构建图字典
st_dict = {}    # 所有线路信息字典
st_list =[]     # 所有站点列表

TEST_DATA = {
    "path": """
        691路:
            索家坟->西直门南->阜成门北->北京儿童医院
        694路:
            北京儿童医院->北京西站->六里桥北里->丰台体育中心->岔路口
        8路:
            岔路口->七里庄->丰台北路->夏家胡同->玉泉营桥西->草桥->洋桥西
        """,
    "counts": 2,
    "stations": 22
}

def show_logo():
    """
    print bus-helper ASCII art logo
    """
    logo = "  ____              _    _      _                 \n" + \
           " |  _ \            | |  | |    | |                \n" + \
           " | |_) |_   _ ___  | |__| | ___| |_ __   ___ _ __ \n" + \
           " |  _ <| | | / __| |  __  |/ _ \ | '_ \ / _ \ '__|\n" + \
           " | |_) | |_| \__ \ | |  | |  __/ | |_) |  __/ |   \n" + \
           " |____/ \__,_|___/ |_|  |_|\___|_| .__/ \___|_|   \n" + \
           "                               | |                \n" + \
           "                               |_|                  "
    print(logo)


def show_menu():
    """
    show client menu
    """
    menu = """Menu:
    -----------------
    1. 设置起点/终点
    2. 搜索所有线路
    3. 搜索最小换乘
    4. 搜索最少途径站点
    -----------------
    6. 查询线路信息
    7. 展示所有线路
    -----------------
    h. 帮助
    q. 退出
    """
    print(menu)


def path_change(path:list):
    """
    将站点路径转化为线路表示, eg:
        X路:
            st0->st1->st2
        换乘x路:
            st2->st3->...
        ...
        总站点数: n
        总换乘数: n
    :param path:路径
    """
    # 谁写的屎山？？？？这我怎么输出？？？
    # 解决方案，找 print 函数，把他们加到 outStr 里面，然后返回
    outStr = ""

    # 屎山全貌
    counts = []
    List_1 = []
    lineList_2 = []
    lineList_1 = []
    lineList = []
    text = st_praser.to_dict()
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
                print("    %s:"%lineList_2[0])
                print("        ",end='')

                # add to outStr
                outStr += "    %s:\n" % lineList_2[0]
                outStr += "        "
                # ----------------

                # temp = path[left, right]
                for i in path[left:right]:
                    print(i,end='')

                    # add to outStr
                    outStr += i
                    # ----------------

                    if i != path[left:right][-1]:
                        print("->",end='')

                        # add to outStr
                        outStr += "->"
                        # ----------------

                print("")

                # add to outStr
                outStr += "\n"
                # ----------------

                List_1 = []
                lineList_2 = []
                left = right - 1
                if right == len(path) - 1:
                    right = right - 1
            if right == len(path) - 1 and len(List_1) != 0:
                lineList.append(List_1[0])
                print("    %s:"%List_1[0])
                print("        ",end='')

                # add to outStr
                outStr += "    %s:\n" % List_1[0]
                outStr += "        "
                # ----------------

                for i in path[left:]:
                    print(i,end='')

                    # add to outStr
                    outStr += i
                    # ----------------

                    if i != path[left:][-1]:
                        print("->",end='')

                        # add to outStr
                        outStr += "->"
                        # ----------------

                print("")

                # add to outStr
                outStr += "\n"
                # ----------------

                List_1 = []
                lineList_2 = []
            right = right + 1
    counts.append(len(lineList) - 1)
    print("    总站点数: %d" %len(path))
    print("    总换乘数: %d" %counts[0])

    lineList = []

    return {
        "path": outStr,
        "counts": counts[0],
        "stations": len(path)
    }


def set_station():
    """
    设置起终点
    """
    # 注意补充相同站点的判断以及空输入的情况判断
    global st,ed,st_list
    st = input("Please set the Start: ")
    is_in = False
    while not is_in:
        is_in = True
        if st not in st_list:
            is_in = False
            print("Error!")
            st = input("Please reset the Start: ")

    is_in = False
    ed = input("Please set the End: ")
    while not is_in:
        is_in = True
        if ed not in st_list or ed == st:
            is_in = False
            print("Error!")
            ed = input("Please reset the End: ")
    
    search.all_path = []
    print("Set succeed!")


def query(query_mode:str):
    """
    查询路径并输出结果, eg:
    方案1:
        X路:
            st0->st1->st2
        换乘x路:
            st2->st3->...
        ...
        总站点数: n
        总换乘数: n
    :param query_mode: '2': 所有线路, '3': 最小换乘, '4': 最少站点
    """
    global st,ed,adj_list
    all_avlb_path = []
    if len(search.all_path) == 0:
        # 在不改变起点站和终点站时，不进行搜索
        search.dfs_search_all(st, ed, adj_list)
    if query_mode == '2':
        for content in search.all_path:
            print("方案%d:" %(search.all_path.index(content)+1))
            all_avlb_path.append(path_change(content))
    elif query_mode == '3':
        for content in route_suggest.min_change(search.all_path):
            print("方案%d:" %(route_suggest.min_change(search.all_path).index(content)+1))
            all_avlb_path.append(path_change(content))
    else :
        for content in route_suggest.min_station(search.all_path):
            print("方案%d:" %(route_suggest.min_station(search.all_path).index(content)+1))
            all_avlb_path.append(path_change(content))
    return all_avlb_path






def get_line_info():
    """
    查询线路信息并返回结果, 格式:
    X路: st->st->st
    """
    global st_dict
    key = input("Query line: ")
    print("%s: " %key, end="")
    for content in st_dict[key]:
        print(content, end="")
        if st_dict[key][-1] != content:
            print("->",end="")
    print("")


def show_all():
    """
    显示所有信息, 格式:
    X路: st->st->st
    """
    global st_dict
    for key in st_dict:
        print("%s: " %key, end="")
        for content in st_dict[key]:
            print(content, end="")
            if st_dict[key][-1] != content:
                print("->",end="")
        print("")


def init():
    """
    initial client
    """
    global adj_list, st_list, st_dict
    show_logo()
    print("正在加载数据...", end="")
    st_praser.load('st.txt')
    st_dict = st_praser.to_dict()
    st_list = st_praser.to_list()
    adj_list = st_praser.to_adj_list()
    print("Done!")
    show_menu()


def main_loop():
    """
    client main loop
    """
    command = ''
    while command != 'q':
        print('Command>', end='')
        command = input()

        if command == '1':
            set_station()
        elif command == 'q':
            print('quit')
        elif command == 'h':
            print('Visit https://github.com/WitchElaina/Beijing-bus-helper#readme for help.')
        elif command == '2' or command == '3' or command == '4':
            query(command)
        elif command == '6':
            get_line_info()
        elif command == '7':
            show_all()
        else:
            print('Invalid Command!')

app = Flask(__name__)
CORS(app)


@app.get('/station/list')
def get_station_list():
    """
    获取所有站点列表
    """
    global st_list
    time.sleep(1)
    return {"stations": st_list}

@app.post('/search')
def search_route():
    """
    搜索路径
    """
    global adj_list, st, ed
    data = request.json
    start = data['start']
    end = data['end']
    print(f"搜索路径: {start} -> {end}")
    # return {"all_path": [TEST_DATA,TEST_DATA]}
    st = start
    ed = end
    search.all_path = []
    all_path = query(2)
    return {"all_path": all_path}


if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', port=5002)