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
