import json
import time
import os

import requests


# 根据alldata内的time进行冒泡排序
def bubbleSort(alldata):
    for w in range(len(alldata) - 1):
        for j in range(len(alldata) - w - 1):
            if alldata[j]['time'] < alldata[j + 1]['time']:
                alldata[j], alldata[j + 1] = alldata[j + 1], alldata[j]
    return alldata


blog_friendlink = 'https://blog.tnxg.top/assets/data/links.json'

data = requests.get(blog_friendlink).json()
t = 0
alldata = []

for i in data:
    print('get:::' + i['link'])
    url = i['rss']
    try:
        jsondata = requests.get(
            'https://api.rss2json.com/v1/api.json?rss_url=' + url, timeout=30)
    except:
        print('Error: ' + url)
        break

    # 设置编码为utf-8
    jsondata.encoding = 'utf-8'
    jsondata = jsondata.json()
    try:
        for n in jsondata['items']:
            title = n['title']
            pubDate = n['pubDate']
            timed = int(time.mktime(time.strptime(
                pubDate, "%Y-%m-%d %H:%M:%S")))
            link = n['link']
            description = n['description']
            categories = n['categories']
            author = i['title']
            alldata.append(
                {'title': title, 'author': author, 'pubDate': pubDate, 'link': link, 'description': description,
                 'categories': categories, 'time': timed})
        print('OK:::' + url)
        t += 1
    except:
        print('Error: ' + url)
        pass

alldata = bubbleSort(alldata)
savedata = json.dumps(alldata, ensure_ascii=False)
# 获取当前文件上级目录的绝对路径
path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# 如果不存在当前目录则创建
if not os.path.exists(path + '/data/friends/'):
    os.makedirs(path + '/data/friends/')
# 检测friends_data.json是否存在
if os.path.exists(path + '/data/friends/data.json'):
    # 如果存在则重命名为friends_data-年-月-日-小时.json
    os.rename(path + '/data/friends/data.json', path + '/data/friends/data-' +
              time.strftime("%Y-%m-%d-%H", time.localtime()) + '.json')
# 文件替换更新
with open(path + '/data/friends/data.json', 'w', encoding='utf-8') as f:
    f.write(savedata)
    print('保存成功')
