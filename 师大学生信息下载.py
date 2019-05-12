import requests
from selenium import webdriver
import time
from lxml import etree
import urllib
from  urllib import request
items=[]
path='D:\chromedriver\chromedriver.exe'
web=webdriver.Chrome(path)
def login():
    url = 'http://jwc.jxnu.edu.cn/Portal/LoginAccount.aspx?t=account'
    web.get(url=url)
    time.sleep(4)
    # name=web.f
    name = web.find_element_by_name('_ctl0:cphContent:txtUserNum')
    password = web.find_element_by_name('_ctl0:cphContent:txtPassword')
    yz = web.find_element_by_name('_ctl0:cphContent:txtCheckCode')

    name.send_keys('201626702050')
    password.send_keys('14243019980306001X')
    yz.send_keys(input('请输入验证码:'))
    print("正在登录....")
    button = web.find_element_by_name('_ctl0:cphContent:btnLogin')
    button.click()
    # time.sleep(3)
    # print(web.get_cookies())
    web.get('http://jwc.jxnu.edu.cn/User/Default.aspx')
    # time.sleep(3)
    web.get(r'http://jwc.jxnu.edu.cn/User/default.aspx?&code=119&&uctl=MyControl\all_searchstudent.ascx')
    # time.sleep(3)
    # print(web.page_source)
    radio = web.find_element_by_id("_ctl1_rbtType_1")
    radio.click()
def get_num():
    option_class = web.find_element_by_name('_ctl1:ddlClass')
    option_school = web.find_element_by_name('_ctl1:ddlCollege')
    option_school_num = option_school.find_elements_by_tag_name('option')
    option_class_num = option_class.find_elements_by_tag_name('option')
    return option_school_num,option_class_num
def deal_msg(text,file):
    tree = etree.HTML(text)
    tr= tree.xpath('//div[@id="contentHolder"]/table/tbody/tr[4]/td/table/tbody/tr')
    for i in tr:
        if i==tr[0]:
            continue
        td=i.xpath('.//td')
        item={
            '所在单位':td[0].text,
            '班级名称':td[1].text,
            '姓名    ':td[2].text,
            '学号    ':td[3].text,
            '性别    ':td[4].text
        }
        # items.append(item)
        file.write(str(item)+'\n')
        # print(td[0].text,td[1].text+'  ',td[2].text+'  ',td[3].text+'  ',td[4].text,)

    # code = str(code_src).strip("'[,]'")
    # code = 'http://jwc.jxnu.edu.cn/Portal/%s' % code
    # print(msg)

def get_msg(file):
    login()
    print("正在读取数据....")
    for a in  range(1,27):
        for b in range(0,len(get_num()[1])):
            option_class_num=get_num()[1]
            # time.sleep(2)
            option_class_num[b].click()
            search = web.find_element_by_name('_ctl1:btnSearch')
            time.sleep(2)
            search.click()
            deal_msg(web.page_source, file)
        option_school_num = get_num()[0]
        option_school_num[a].click()

def main():
    file=open(r'C:\Users\cy\Desktop\师大学生信息.txt','a')
    get_msg(file)
    file.close()



if __name__ == '__main__':
    main()