import requests
from bs4 import BeautifulSoup
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}


def get_url(or_str:str):
    """
    get url from html string
    :param or_str: original html string, with tile and url
    :return: title and url
    """
    url_st = or_str.find('href=\"') + 6
    url_ed = or_str.find('\" tar')
    title_st = or_str.find('\">') + 2
    title_ed = or_str.find('</a')
    title = or_str[title_st:title_ed]
    url_ = or_str[url_st:url_ed]
    # print(title, end=': ')
    # print(url_)
    return title, url_


def get_url_dict(filename):
    """
    get url dict from 'filename.txt'
    :param filename: txt filename
    :return: url dict, { roadName: url, ... }
    """
    ret = {}
    with open(filename, 'r') as url_file:
        for line in url_file:
            # print(line)
            if line.find('<a') != -1:
                cur_title, cur_url = get_url(line)
                ret[cur_title] = cur_url
    # print(len(ret))
    return ret


def get_road_info(title, url):
    ret = ''
    res = requests.get(url, headers=headers)
    bs = BeautifulSoup(res.text, 'lxml')
    stations = bs.find_all('input', id='stationNames')
    for info in stations:
        st = str(info).find('value=\"') + 7
        ed = str(info).find('\"/>')
        station_str = str(info)[st:ed]
        st_list = station_str.split(',')
        ret = title + '->' + str(st_list)
        print(ret)
    if stations == []:
        raise Exception
    return ret



if __name__ == '__main__':
    url_dict = get_url_dict('urls.txt')
    err_list = []
    with open('st.txt', 'w') as res:
        for st_name in url_dict.keys():
            print('Getting ', end=str(st_name)+':...')
            try:
                cur = get_road_info(str(st_name), url_dict[st_name])
            except Exception as err:
                print(err)
                with open('err.txt', 'w') as errs:
                    errs.writelines(str(st_name)+'=>'+url_dict[st_name]+'\n')
            else:
                res.writelines(cur+'\n')
                print('Succeed!')
                print('Waiting...')
                time.sleep(2)



