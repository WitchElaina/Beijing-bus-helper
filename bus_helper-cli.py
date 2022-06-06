"""
bus helper command line client
"""

import search
import route_suggest
import st_praser

st = ""
ed = ""
adj_list = {}
st_dict = {}
st_list =[]

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


def set_station():
    """
    设置起终点
    """
    # todo


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
    # todo


def get_line_info():
    """
    查询线路信息并返回结果, 格式:
    X路: st->st->st
    """
    # todo


def show_all():
    """
    显示所有信息, 格式:
    X路: st->st->st
    """
    # todo

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
    # todo
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
        # todo ....
        else:
            print('Invalid Command!')


if __name__ == '__main__':
    init()
    main_loop()
