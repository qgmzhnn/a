import requests
import time
from lxml import etree
from queue import Queue
import threading
import os
import re
import json
import urllib
import execjs
from urllib import request
from selenium import webdriver
import hashlib
import execjs
path='D:\chromedriver\chromedriver.exe'

get_list=[]
download_list=[]
url_list=[]
x=1
headers = {
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
    # 'Referer':''
}

class download_thread(threading.Thread) :
    def __init__(self,name,url_queue):
            threading.Thread.__init__(self)
            self.name=name
            self.url_queue=url_queue
    def run(self) :
        global x
        print('%s--启动' % self.name)
        while True:
            # time.sleep(3)
            if self.url_queue.empty():
                print('%s----结束' % self.name)
                break
            url=self.url_queue.get()
            # print("玩命下载中...")
            urllib.request.urlretrieve(url,r"C:/Users/cy/Desktop/movie1/%s.ts"%x)
            x+=1
def from_data(url,md5):
    data = {
        'type' : 'migu',
        'siteuser' : '',
        'md5' : md5,
        'lg' : '',
        'id' : '654574536',
        'hd' : '',
    }
    return data
def get_urllist(url,md5):
    r = requests.post(url="http://69p.top/md/url.php", headers=headers, data=from_data(url,md5))
    data = json.loads(r.text)
    print(data)
    movie_url = data['url']
    r = requests.get(url=movie_url)
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[~]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    # pattern = re.compile('^#')
    url_list = pattern.findall(r.text)
    return url_list

def create_queue(list):

    url_queue=Queue()
    for i in list:
        url_queue.put(i)
    return url_queue
#

def create_download_movie(url_queue):
    name2 = ['解析器1号', '解析器2号', '解析器3号']
    for name in name2 :
        tdownload = download_thread(name,url_queue)
        download_list.append(tdownload)
def hebing():
    os.system(r"copy/b C:\Users\cy\Desktop\movie1\*.ts C:\Users\cy\Desktop\a.mp4")
def get_js():
    f = open(r'C:\Users\cy\Desktop\tools.js', 'r', encoding='utf-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr
def get_md5():
    url=input('请输入视频链接。。。')
    web = webdriver.Chrome(path)
    web.get(url='http://69p.top/?url={}'.format(url))
    # md5="document.querySelector('#hdMd5')"
    url=web.find_element_by_xpath('//iframe[@id="player"]').get_attribute('src')
    web.switch_to.frame('player')
    a = web.find_element_by_xpath('//input[@id="hdMd5"]').get_attribute('value')
    web.close()
    code = a + '!abef987'
    s = hashlib.md5()
    s.update(code.encode('utf-8'))
    code = s.hexdigest()
    # print(code)
    # print (s
    jsstr = get_js()
    # print (jsstr)
    ctx = execjs.compile(jsstr)
    md5 = ctx.call('sign', code)
    return md5,url
def main():
    md5,url=get_md5()
    list=get_urllist(url,md5)
    url_queue= create_queue(list)
    # create_get_url()
    create_download_movie(url_queue)
    for i in download_list:
        i.start()
    for i in download_list :
        i.join()
    # hebing()
    print("down")
if __name__ == '__main__':
    main()