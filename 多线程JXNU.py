from threading import Thread
import threading
from selenium import webdriver
import time
from queue import   Queue
from  lxml import etree
path='D:\chromedriver\chromedriver.exe'
web=webdriver.Chrome(path)
a=1
name_list=[]
name_list1=[]
class get_thread(threading.Thread):
    def __init__(self,name,read_queue):
        threading.Thread.__init__(self)
        self.name=name
        self.read_queue=read_queue

    def run(self):
        print('%s---已启动'%self.name)
        # while True:
        #     if self.read_queue.empty():
        #         print('%s---已结束'%self.name)
        #         break
        msg=self.read_queue.get()
        deal_msg(msg)

class read_thread(threading.Thread):
    def __init__(self,name,read_queue):
        threading.Thread.__init__(self)
        self.name=name
        self.read_queue=read_queue

    def run(self):
        print('%s---已启动'%self.name)
        get_msg(self.read_queue)



def login():
    url = 'http://jwc.jxnu.edu.cn/Portal/LoginAccount.aspx?t=account'
    web.get(url=url)
    time.sleep(4)
    # name=web.f
    name = web.find_element_by_name('_ctl0:cphContent:txtUserNum')
    password = web.find_element_by_name('_ctl0:cphContent:txtPassword')
    yz = web.find_element_by_name('_ctl0:cphContent:txtCheckCode')
    name.send_keys('学号')
    password.send_keys('密码')
    yz.send_keys(input('请输入验证码:'))
    button = web.find_element_by_name('_ctl0:cphContent:btnLogin')
    button.click()
    time.sleep(3)
    # print(web.get_cookies())
    web.get('http://jwc.jxnu.edu.cn/User/Default.aspx')
    time.sleep(3)
    web.get(r'http://jwc.jxnu.edu.cn/User/default.aspx?&code=119&&uctl=MyControl\all_searchstudent.ascx')
    time.sleep(3)
    # print(web.page_source)
    radio = web.find_element_by_id("_ctl1_rbtType_1")
    radio.click()
def get_num():
    option_class = web.find_element_by_name('_ctl1:ddlClass')
    option_school = web.find_element_by_name('_ctl1:ddlCollege')
    option_school_num = option_school.find_elements_by_tag_name('option')
    option_class_num = option_class.find_elements_by_tag_name('option')
    return option_school_num,option_class_num
def deal_msg(text):
    tree = etree.HTML(text)
    tr= tree.xpath('//div[@id="contentHolder"]/table/tbody/tr[4]/td/table/tbody/tr')
    i=1
    for i in tr:
        td=i.xpath('.//td')
        print(td[0].text,td[1].text+'  ',td[2].text+'  ',td[3].text+'  ',td[4].text,)
def  create_get_thread(read_queue):
    thread_name={'解析器1号'}
    for name in thread_name:
        tget=get_thread(name,read_queue)
        name_list.append(tget)
def  create_read_thread(read_queue):
    thread_name={'采集器1号'}
    for name in thread_name:
        tget=read_thread(name,read_queue)
        name_list1.append(tget)
def create_queue():
    read_queue=Queue()
    return read_queue
def get_msg(read_queue):
    global a
    for a in  range(27):
        for b in range(len(get_num()[1])):
            read_queue.put(web.page_source)
            option_class_num=get_num()[1]
            # time.sleep(2)
            option_class_num[b].click()
            search = web.find_element_by_name('_ctl1:btnSearch')
            time.sleep(2)
            search.click()

        option_school_num = get_num()[0]
        option_school_num[a].click()
        a+=1

def main():
    read_queue=create_queue()
    login()
    create_get_thread(read_queue)
    create_read_thread(read_queue)
    for name in name_list1:
        name.start()
    for name in name_list:
        name.start()
    for name in name_list :
        name.join()
    for name in name_list1 :
        name.join()

    print("down")



if __name__ == '__main__':
    main()
