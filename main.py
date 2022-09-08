# This is a sample Python script.
import datetime
import os

import requests
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def save_image(image_url, root, image_name):
    splits = image_url.split('.')
    path = root + image_name + '.' + splits[-1]
    print('image path: ', path)
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(image_url)
            r.raise_for_status()
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                print('文件保存成功')
        else:
            print('文件已存在')
    except Exception as e:
        print('爬取失败', e)


def crawl_html(root):
    start_date = datetime.datetime.strptime('2021.02.01', '%Y.%m.%d')
    end_date = datetime.datetime.now()
    while start_date < end_date:
        print(start_date)
        str_date = start_date.strftime('%Y-%m')
        image_view_url = 'https://bing.wdbyte.com/{}.html'.format(str_date)
        root_path = root + str_date + '/'
        parse_html(image_view_url, root_path)
        start_date = start_date + relativedelta(months=1)


def parse_html(image_view_url, root):
    response = requests.get(image_view_url)
    print(response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_div_list = soup.find_all("div", {"class": "w3-third"})
        for image_div in image_div_list:
            image_name_text = image_div.find_next('p').text
            image_name = image_name_text[0:10].replace('-', '').strip()
            image_url = image_div.find_next('p').find_next('a')['href']
            print(image_name, image_url)
            save_image(image_url, root, image_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    crawl_html('D:/wallpaper/')
