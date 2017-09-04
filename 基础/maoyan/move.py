# -*- coding: utf-8 -*-
import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return  None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?<i class="board-index.*?">(.*?)</i>'
                         +'.*?<img data-src="(.*?)" alt="(.*?)" class="board-img" />'
                         +'.*?<p class="star">(.*?)</p>',re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:]
        }

def write_to_file(content):
    with open('result.txt', 'a') as f:
        f.write(json.dumps(content) + '\n')
        f.close




def main(offest):
    url = 'http://maoyan.com/board/4?offset='+str(offest)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print item
        write_to_file(item)


if __name__ =='__main__':
    for i in range(10):
        main(i*10)
    pool = Pool()
    pool = map(main, [i*10 for i in range(10)])

