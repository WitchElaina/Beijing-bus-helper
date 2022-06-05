# Beijing-bus-helper

USTB人工智能大作业, 北京公交换乘助手

## Development

### 数据获取

使用爬虫获取数据, 目标网站为https://bus.mapbar.com/

观察网站结构后发现, 网站有一个导航页收录了所有北京公交线路的URL, 因此可以首先对该导航页进行爬取, 获得所有线路的URL

#### 获取URL

观察导航页的html源码, 发现所有url都被存放在`<dd>`标签中, 因此只需找到这些元素即可, 代码如下

```python
# url_robot.py
import requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'
}
url_home = 'https://bus.mapbar.com/beijing/xianlu/'
res = requests.get(url_home, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

# get all <dd></dd> DOM elements
all_url = soup.find_all('dd')

# output
#   use 'python3 url_robot.py > urls.txt' to redirect all urls to txt file
for i in all_url:
    print(i)
```

将输出重定向至`url.txt`, 方便以后读取
```shell
python3 url_robot.py > urls.txt
```

在`url.txt`中会得到以下格式的字符串
```text
<dd>
<a href="http://bus.mapbar.com/beijing/xianlu/1lu/" target="_blank" title="北京1路公交线路 ">1路</a>
...
```

#### 获取站点信息

接下来需要访问每条线路的URL, 随后抓取站点信息, 分析html源码后发现线路信息都存放在`id`属性为`stationName`的标签内, 因此只需找到这些元素即可

```python
res = requests.get(url, headers=headers)
bs = BeautifulSoup(res.text, 'lxml')
stations = bs.find_all('input', id='stationNames')
```

上述代码会将获得的html代码存储在`station`中, 格式类似
```html
<input type="hidden" value="老山公交场站,老山南路东口,地铁八宝山站,玉泉路口西,永定路口东,五棵松桥西,沙沟路口西,东翠路口,万寿路口西,翠微路口,公主坟,军事博物馆,木樨地西,工会大楼,南礼士路,复兴门内,西单路口东,天安门西,天安门东,东单路口西,北京站口东,日坛路,永安里路口西,大北窑西,大北窑东,郎家园,四惠枢纽站" id="stationNames">
```

接下来利用字符串查找等相关操作提取出`value`中的元素, 然后`split(',')`按`,`分隔开, 即可得到站点列表, 将上述操作封装成`get_road_info`函数以便重复调用,
最终代码如下

```python
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
```

核心功能完成后, 剩下的都是一些简单的工作, 如从先前的`url.txt`中提取`URL`, 将获得的站点信息格式化后写入文件

> ps.为了防止请求过快被服务器ban掉ip, 需要设置一定的冷却时间, 这无疑会导致程序运行时间增加, 恰好手边有台闲置的服务器, 最终在服务器上运行完成了数据爬取

完整代码如下:
```python
# per_rebot.py
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
```

最终结果保存在`st.txt`中, 格式如下:

```text
线路名称->['站点', '站点', ...]
11路->['大北窑东', '八王坟南', '北京东站北', '九龙山', '珠江帝景', '大郊亭桥西', '大郊亭桥东', '东石门', '唐家村', '小海子', '四根旗杆', '方家村', '朝阳半壁店', '观音堂北', '观音堂', '古塔公园', '王四营', '王四营桥东', '孛罗营村北', '孛罗营']
```

### 数据处理

站点存储采用txt方式进行纯文本存储, 读取时调用`st_prase.py`中的方法

其中`to_adj_list`方法会返回一个邻接表用于后续构建图结构


### 路径搜索

使用深度优先+递归的方法搜索, 搜索一个节点是否为目标节点, 如果不是则以其子节点为起点, 递归调用搜索函数

由于站点较多, 需要进行剪枝, 实际生活中, 不会换乘较多次数, 因此编写剪枝函数`pruning`, 以当前路径换乘次数为标准, 超过一定次数后放弃此路径的搜索

### 方案选优

搜索完成后, 需要根据用户需求进行选优, `min_change`方法用于获取路径中最少换乘的路径, `min_station`方法用于获取距离最短(经过最少站点)的路径

> ps. 如果有平行方案会全部输出
