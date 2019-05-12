import requests
import re
import execjs
from lxml import etree
import csv
headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
def get_js():
    file=open(r'C:\Users\cy\Desktop\guazi.js', 'r', encoding='utf-8')
    line=file.readline()
    text=''
    while line:
        text=text+line
        line=file.readline()
    return text
def get_text():
    s=requests.session()
    r=s.get('https://www.guazi.com/cc/buy/',headers=headers)

    r.encoding='urf-8'
    text=r.text
    print(text)
    text='eval'+re.findall('eval(.*?)var name',text)[0].replace('var value=','return ')# 不加return计算的value值是错误的！！！！！！
    ctx=execjs.compile(text)
    value=ctx.call('anti')
    ctx2=execjs.compile(get_js())
    cookie=ctx2.call('xredirect','antipas',value,'')
    new_headers={
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
         'Cookie': cookie
    }
    r=requests.get('https://www.guazi.com/cc/buy/',headers=new_headers)
    return r.text
def get_msg(file):
    text=get_text()
    tree=etree.HTML(text)
    cars=tree.xpath('//ul[@class="carlist clearfix js-top"]/li')
    for car in cars:
        name=car.xpath('.//a')[0].attrib['title']
        href='https://www.guazi.com'+car.xpath('a')[0].attrib['href']
        year=car.xpath('a/div[1]/text()')[0]
        gongli=car.xpath('a/div[1]/text()[2]')[0]
        fuwu=car.xpath('a/div[1]/text()[3]')[0]
        try:
            price_low="折后价:"+car.xpath('a/div[2]/p/text()')[0]+'万'
            price = "原价:" + car.xpath('a/div[2]/em/text()')[0]
            butie = ''
        except:
            price_low='补贴后'+car.xpath('a/div[2]/p/text()')[0]+'万'
            butie=car.xpath('a/em/text()[1]')[0]+car.xpath('a/em/span/text()')[0]+"元"
            price = ''
        try:
            jishou=car.xpath('a/div[2]/i[2]/text()')[0]
            if jishou !='急售':
                jishou = car.xpath('a/div[2]/i[1]/text()')[0]
                if jishou != '急售' :
                    jishou=''
        except:
                jishou = ''
        try :
            chaozhi = car.xpath('a/div[2]/i[1]/text()')[0]
            if chaozhi!='超值':
                chaozhi=''
        except   :
            chaozhi = 'none'
        try :
            xinche = car.xpath('a/div[2]/i[1]/text()')[0]
            if xinche != '准新车':
                xinche = car.xpath('a/div[2]/i[2]/text()')[0]
                if xinche != '准新车':
                    xinche = ''
        except :
            xinche = ''
        file.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(name,year,gongli,fuwu,price_low,price,butie,"严选车",jishou,chaozhi,xinche,href))


if __name__ == '__main__':
    with open('瓜子.csv','w',newline='') as file:
        csv_writer = csv.writer(file, dialect='excel')
        csv_writer.writerow(["车辆详情", "上牌时间", "行驶公里",'服务类型', "优惠价", "原价","补贴金", "严选", "急售" , "超值", "新车", "详细地址"])
        get_msg(file)
        print("Down")
        file.close()