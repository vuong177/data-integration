import csv
from http.client import responses
import bonobo
from pkg_resources import yield_lines
import requests
from bonobo.config import use_context_processor
from bonobo.config import use
import time
import pandas
from bs4 import BeautifulSoup
from requests_html import HTMLSession  
import pandas

import json

def getPage(i):
    objects = []
    url = f"https://www.nguyenkim.com/dien-thoai-di-dong/page-{i}/";
    response = requests.get(url).text
    soup = BeautifulSoup(response, features="lxml")

    container_items = soup.find('div', {'id': 'pagination_contents'})    

    items = container_items.find_all("a", {"class": "product-render"})
    for item in items:
        object = {}
        href = item.get("href")
        object['url'] = f"{href}"
        object['name'] = item.get("name")
        object['image'] = item.get("link")
        objects.append(object)
    return objects

def extractPhones():
    for i in range(1,3):
        objects = getPage(i)
        for object in objects:
            yield object

def basicInfo(*args):

    url = args[0]['url']

    response = requests.get(url).text
    soup = BeautifulSoup(response, "html.parser")
    # print(response)

    object_phone = {}

    object_phone['name'] = args[0]['name']
    object_phone['url'] = args[0]['url']
    object_phone['image'] = args[0]['image']

    div_contain = soup.find("div", {"id": "productSpecification_fullContent"})

    table = div_contain.find("table", {"class": "productSpecification_table"})

    rows = table.find_all("tr")
    for row in rows:
        data = row.find_all("td")
        label_html = data[0]
        value_html = data[1]
        label = label_html.getText().replace(',', ' ').replace(';',' ').replace(':', '')
        value = value_html.getText().replace(',', ' ').replace(';',' ').replace(':', '')
        object_phone[label] = value

    yield object_phone


def loadPhones_thread1(*args):
    fields = ['name', 'url', 'image', 'Model', 'Màu sắc',
        'Nhà sản xuất', 'Xuất xứ', 'Năm ra mắt ', 'Thời gian bảo hành', 
        'Địa điểm bảo hành', 'Hệ điều hành', 'Camera trước', 'Camera sau', 'Đèn Flash', 'Video', 
        'Mạng 4G', 'Loại SIM', 'WIFI', 'Bluetooth', 'GPS', 'USB', 'Jack 3.5mm']
    data = []
    for field in fields:
        if field in args[0].keys():
            data.append(str(args[0].get(field)))
        else:
            data.append("")
    yield data, 1

def loadPhones_thread2(*args):
    fields = ["name", 'Hệ điều hành', 'Chipset', 'RAM', 'Bộ nhớ trong', 
        'Hỗ trợ thẻ nhớ ngoài', 
        'Độ phân giải màn hình', 'Camera trước', 'Camera sau', 'Đèn Flash', 'Video', 
        'Mạng 4G', 'Loại SIM', 'WIFI', 'Bluetooth', 'GPS', 'USB', 'Jack 3.5mm']        
    data = []

    for field in fields:
        if field in args[0].keys():
            data.append(str(args[0].get(field)))
        else:
            data.append("")
    separate = ';'
    line = separate.join(data)

    yield data, 2

def compose_thread(*args):
    ans = []
    data = args[0]
    if args[1] == 2 :
        return
    compose =  data
    separate = ';'
    line = separate.join(compose)
    with open ("/Users/vuong/data-integration/Bonobo/Bonobo/data/nk.csv", "a") as f:
        f.write(line+"\n")



def get_graph(**options):
    graph = bonobo.Graph()
    graph >> extractPhones >> basicInfo >> loadPhones_thread1 >> compose_thread
    graph.get_cursor(basicInfo) >> loadPhones_thread2 >> compose_thread

    return graph


def get_services(use_cache=False):
    return {}


if __name__ == '__main__':
    parser = bonobo.get_argument_parser()
    with bonobo.parse_args(parser) as options:
        bonobo.run(get_graph(**options), services=get_services(**options))