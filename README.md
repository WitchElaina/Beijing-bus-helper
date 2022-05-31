# Beijing-bus-helper
USTB人工智能大作业, 北京公交换乘助手
## Development
### 数据获取
使用爬虫获取数据, 目标网站为https://bus.mapbar.com/

首先从该网站的导航页爬取每条公交线路的URL, 随后从获得的URL中获取每条线路的信息

在处理DOM结构时需要用到beautifulsoup4, 首先进行安装
```shell
pip3 install beautifulsoup4
```
