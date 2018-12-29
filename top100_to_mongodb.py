'''
抓取猫眼电影排行
'''
import re
import time
import pymongo
import requests
from requests.exceptions import RequestException
from fake_useragent import UserAgent

def get_one_page(url):
    """获取url的电影信息"""
    try:
        uat = UserAgent()
        headers = {
            'User-Agent': uat.random
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """解析单页电影信息"""
    pattern = re.compile(r'<dd>.*?board-index-.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }


def write_to_mongodb(data):
    """写入MongoDB数据库"""
    # 创建数据库需要使用 MongoClient 对象，并且指定连接的 URL 地址和要创建的数据库名。
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # 创建数据库test和集合collections，注意使用[]
    mydb = myclient["test"]
    mycol = mydb["top100"]
    mycol.insert_one(data)


def main(offset):
    """main()"""
    url = 'https://maoyan.com/board/4?offset='+ str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_mongodb(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1.5)
