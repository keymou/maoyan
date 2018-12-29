'''
抓取猫眼电影排行
'''
import csv
import json
import re
import time
import requests
from requests.exceptions import RequestException

def get_one_page(url):
    """获取url的电影信息"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
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


def write_to_txt(content):
    """写入txt文件"""
    with open('movie_top100.txt', 'a', encoding='utf-8') as f:
        print(type(json.dumps(content)))
        f.write(json.dumps(content, ensure_ascii=False)+'\n')


def save_txt():
    """爬虫结果保存到txt文件"""
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset=' + str(i*10)
        html = get_one_page(url)
        for item in parse_one_page(html):
            print(item)
            write_to_txt(item)
        time.sleep(2)


def write_to_header(header):
    """csv文件头"""
    with open('movie_top.csv', 'a', newline='') as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(header[0])

def write_to_csv(data):
    """写入csv文件"""
    with open('movie_top.csv', 'a', newline='') as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(data.values())

def save_csv():
    """爬虫结果保存到csv文件"""
    url = 'https://maoyan.com/board/4'
    html = get_one_page(url)
    header = []
    for itme in parse_one_page(html):
        header.append(list(itme.keys()))
    write_to_header(header)
    for i in range(10):
        url = 'https://maoyan.com/board/4?offset='+ str(i*10)
        html = get_one_page(url)
        for item in parse_one_page(html):
            write_to_csv(item)
        time.sleep(2)
