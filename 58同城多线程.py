import threading
import requests
import re
from lxml import etree
from queue import Queue
import time
import random
import base64
from fontTools.ttLib import TTFont
import csv
get_list=[]
deal_list=[]

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}


class get_urls(threading.Thread):
    def __init__(self,name,page_queue,url_queue):
        threading.Thread.__init__(self)
        self.name=name
        self.page_queue=page_queue
        self.url_queue=url_queue
    def run(self):
        print('%s--启动' % self.name)
        while True:
            if self.page_queue.empty():
                print('%s----结束' % self.name)
                break
            time.sleep(random.uniform(1,5))
            r=requests.get(url='https://nc.58.com/chuzu/?utm_source=market&spm=u-2d2yxv86y3v43nkddh1.BDPCPZ_BT&PGTID=0d100000-0029-da6e-39ec-e3ff84ddde29&ClickID=%s'%self.page_queue.get(),headers=headers)
            text=r.text
            tree=etree.HTML(text)
            list=tree.xpath('//div[@class="listBox"]/ul/li')
            for i in list:
                try:
                    url=i.xpath('div[1]/a/@href')[0]
                    self.url_queue.put(url)
                    # print(url)
                except:
                    pass
class get_msgs(threading.Thread) :
    def __init__(self, name, url_queue,lock,file) :
        threading.Thread.__init__(self)
        self.name = name
        self.url_queue = url_queue
        self.lock=lock
        self.file=file

    def run(self) :
        time.sleep(1)
        print('%s--启动' % self.name)
        while True:
            # if self.url_queue.empty():
            #     print('%s----结束' % self.name)
            #     break
            try:
                time.sleep(random.uniform(1,5))
                text=get_text(self.url_queue)
                tree = etree.HTML(text)
                type = tree.xpath('//div[@class="house-desc-item fl c_333"]/div[1]/span[2]/text()')[0]
                price = tree.xpath('//div[@class="house-pay-way f16"]/span[1]/b/text()')[0]
                phone = tree.xpath('//div[@class="house-chat-phonenum"]/p[3]/text()')[0]
                hourse = str(tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[2]/span[2]/text()')[0]).replace(
                    '&nbsp', '').replace(' ','')
                loucen = str(tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[3]/span[2]/text()')[0])
                xiaoqu = tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[4]/span[2]/a/text()')[0]
                diqu = tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[5]/span[2]/a[1]/text()')[0] + \
                       tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[5]/span[2]/a[2]/text()')[0]
                addr = str(tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[6]/span[2]/text()')[0]).lstrip()
                self.lock.acquire()
                self.file.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(price, type, phone, hourse, loucen,xiaoqu,diqu,addr))
                self.lock.release()
            except Exception as  e:
                print(e)

def get_text(url_queue):
    '''页面刷新，字符的对应关系也会刷新'''
    r=requests.get(url=url_queue.get(),headers=headers)
    font_face=str(re.findall("base64,(.*?)\)",r.text)[0]).replace("'",'')
    b = base64.b64decode(font_face)
    with open('58同城.ttf', 'wb')as f :
        f.write(b)
    font=TTFont('58同城.ttf')
    font.saveXML('58同城.xml')
    text=r.text
    # print(text)
    tree=etree.HTML(text)
    price=tree.xpath('//div[@class="house-pay-way f16"]/span[1]/b/text()')[0]
    phone=tree.xpath('//div[@class="house-chat-phonenum"]/p[3]/text()')[0]

    hourse=str(tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[2]/span[2]/text()')[0]).replace('室','').replace('厅','').replace('卫','').replace('平  精装修 ','').split()
    hourse=hourse[0]+hourse[1]
    loucen=str(tree.xpath('//div[@class="house-desc-item fl c_333"]/ul/li[3]/span[2]/text()')[0]).split('/')[1].replace('层','').replace(' ','')



    '''将提取出的乱码解为数字'''
    '''先取出所有的乱码，放到一个list中，遍历这个list，转换乱码编码格式再放入一个list2中，
        遍历list2，将其转换为十进制，放到list3中，遍历llist3，在ttf文件中cmp属性下找到对应的值放到
        list4中，将list3和list4分别作为key和value组成字典，最后遍历字典，将源码中的乱码替换
    '''
    luanma=append(price + phone + hourse + loucen)
    bianma,cmp=deal(luanma,font)
    # print(cmp)
    for i in bianma:
        try:
             text = text.replace(str(i),cmp[i])

        except Exception as e:
            print(e)
    return text
def deal(luanma,font):
    shuzi = []
    bianma = []
    msg_tran = []
    cmp = {}
    uni_list = font.getGlyphOrder()[1 :]
    obj = font['cmap']
    obj = obj.getBestCmap()  # 获得map映射关系
    '''将乱码都转为unicode_escape格式'''
    for i in luanma:
        a = str(i.encode('unicode_escape'))  # 将中文乱码转为16进制编码
        b = a.replace("\\", ',').replace("'", '').replace('u', '').split(",,")[1]
        if b not in msg_tran:
            msg_tran.append(b)
    '''拼接字符'''
    for i in range(0, len(msg_tran)) :
        a = '&#x' + str(msg_tran[i])+';'  # 还原为爬取的内容中的格式
        bianma.append(a)
    '''找到对应的值'''
    for i in luanma :
        ten = ord(i)  # 将字符转为十进制
        gly = obj[ten]
        if int(gly[-1 :]) != 0 :
            new_data =str(int(gly[-1 :]) - 1)  # 解密后的数字为name属性的最后一个数字减去一
            if new_data not in shuzi:
                shuzi.append(new_data)
        else :
            new_data =str(9)
            if new_data not in shuzi :
                shuzi.append(new_data)
    '''组成字典'''
    for i in range(0,len(shuzi)):
        cmp.setdefault(bianma[i],shuzi[i])
    return bianma,cmp
def append(msg):
    luanma = []

    for i in msg :
        if i not in luanma :
            luanma.append(i)
    return luanma
def  create_thread(page_queue,url_queue,lock,file):
    name1 = ['采集器1号', '采集器2号', '采集器3号']
    name2 = ['解析器1号', '解析器2号', '解析器3号']
    for name in name1:
        get=get_urls(name,page_queue,url_queue)
        get_list.append(get)
    for name in name2 :
        deal = get_msgs(name, url_queue,lock,file)
        deal_list.append(deal)
def create_queue():
    page_queue=Queue()
    url_queue=Queue()
    for i in range(1,10):
        page_queue.put(i)
    return  page_queue,url_queue
def main():

    with open('58同城.csv','w',newline='',encoding='utf-8') as file:
        csv_writer=csv.writer(file,dialect='excel')
        csv_writer.writerow(["价格", "方式",'电话', "房屋类型", "朝向楼层", "所在小区", "所属区域", "详细地址"])
        page_queue, url_queue = create_queue()
        lock = threading.Lock()
        create_thread(page_queue, url_queue, lock, file)
        for i in get_list:
            i.start()
        for i in deal_list :
            i.start()
        print('玩命下载中.....')
        for i in get_list :
            i.join()
        for i in deal_list :
            i.join()

    print('Down')
    file.close()


if __name__ == '__main__':
    main()