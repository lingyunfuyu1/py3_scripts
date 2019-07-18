# -*- coding: utf-8 -*-
import logging
import re
import time
import traceback

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# 通用HTTP请求头
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 't66y.com',
    'Referer': 'http://t66y.com/',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}

proxies = {
        'http': 'http://127.0.0.1:1080',
        'https': 'http://127.0.0.1:1080',
    }


def get_post_urls():
    post_urls = []
    url = 'http://t66y.com/thread0806.php?fid=7&search=today'
    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
        response.encoding = 'gbk'
        if response.text.find('技術討論區') == -1:
            logger.info('查找失败！HTTP响应内容为：\n' + response.text)
            return post_urls
        soup = BeautifulSoup(response.text, 'html.parser')
        h3s = soup.find_all('h3')
        for h3 in h3s:
            href = h3.a.get('href').strip()
            title = h3.a.text.strip()
            if href.startswith('htm_data') and title.find('码') != -1:
                post_urls.append(href)
        return post_urls
    except:
        logger.info('发生未知异常：' + traceback.format_exc())
        return post_urls

def get_codes(post_url):
    codes = []
    try:
        response = requests.get(post_url, headers=headers, proxies=proxies, timeout=30)
        response.encoding = 'gbk'
        if response.text.find('技術討論區') == -1:
            logger.info('查找失败！HTTP响应内容为：\n' + response.text)
            return codes
        soup = BeautifulSoup(response.text, 'html.parser')
        post_content = soup.find(attrs={'class': 'tpc_content do_not_catch'}).text
        results = re.findall('\W([A-Za-z0-9_*#@]{16})\W', post_content)
        for result in results:
            count = 0
            for ch in '_*#@':
                count += result.count(ch)
            if count <= 2:
                codes.append(result)
        return codes
    except:
        logger.info('发生未知异常：' + traceback.format_exc())
        return codes


def main():
    while True:
        try:
            post_urls = get_post_urls()
            if len(post_urls) == 0:
                print('今日主题无发码贴')
            for post_url in post_urls:
                post_url = 'http://t66y.com/' + post_url
                print('帖子地址：' + post_url)
                codes = get_codes(post_url)
                if len(codes) == 0:
                    print('当前帖子无邀请码')
                for code in codes:
                    print(code)
                print()
                time.sleep(3)
            time.sleep(60)
        except:
            logger.info('发生未知异常：' + traceback.format_exc())


if __name__ == '__main__':
    main()
