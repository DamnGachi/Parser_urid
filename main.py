import json
import os
import re
from datetime import date

import requests
from bs4 import BeautifulSoup

# from send_email import create_letter


ress = []
sss = []
urls = []
all_categories_test = {}
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

# Make an HTTP request to the website

r = requests.get(url="https://www.consultant.ru/popular/", headers=headers)
if not os.path.exists("data"):
    os.mkdir("data")

with open("data/page_1.html", "w", encoding='utf-8') as file:
    file.write(r.text)

with open("data/page_1.html", encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
res = []
all_news = soup.find('div', class_='col-pt-9 col-pt-push-3').find_all("a")
for item in all_news:
    item_url = item.get('href')
    res.append(item_url)
for i in res[3:]:
    if i.split('/')[1] == 'document':
        urls.append(i)


def collecting_data():
    for url in urls:

        r = requests.get(url="https://www.consultant.ru/" + url, headers=headers)
        if not os.path.exists("data1"):
            os.mkdir("data1")

        with open("data1/page_1.html", "w", encoding='utf-8') as file:
            file.write(r.text)

        with open("data1/page_1.html", encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find('div', class_='document__insert doc-insert')
        if all_news is not None:
            sss.append((all_news.find_all("a"))[0].get('href'))
    print('x1')


def collecting_data1():
    for url in sss:

        r = requests.get(url="https://www.consultant.ru/" + url, headers=headers)
        if not os.path.exists("data2"):
            os.mkdir("data2")

        with open("data2/page_1.html", "w", encoding='utf-8') as file:
            file.write(r.text)

        with open("data2/page_1.html", encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        all_news = soup.find('div', class_='document-page__content document-page_left-padding')
        all_newss = soup.findAll('p', class_='no-indent')
        if all_news is None:
            continue
        s = (re.findall(r"[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}", (all_news.text)))

        dt = date.today()
        dt = dt.strftime("%d.%m.%Y")

        if str(dt) == s[0]:
            for item in all_newss:
                item_url = item.find('strong', string=re.compile('стать'))
                item_url1 = item.find('a', string=re.compile('Изменение|изложена|Дополнение'))
                if item_url is None:
                    continue
                item_get1 = item_url.getText()

                if item_url1 is None:
                    continue
                item_get = "https://www.consultant.ru/" + item_url1.get('href')

                all_categories_test[item_get1] = item_get

                with open('all_categories_test.json', 'w', encoding='utf-8') as file:
                    json.dump(all_categories_test, file, indent=4, ensure_ascii=False)
    from send_email import create_letter
    return create_letter()


if __name__ == '__main__':
    collecting_data()
    collecting_data1()
