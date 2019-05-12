import requests
import re
from lxml import etree
import lxml
shanghu=[]
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}
'''大众点评_token生成过程，jv为http://www.dianping.com?shopId=6585548样式'''
js='''
    iP.reload = function(jv) { 
                    var jw;
                    var jx = {};
                    if (typeof jv === _$_543c[91]) {
                        jx = iO.parse(jv.split(_$_543c[146])[1])
                    } else {
                        if (typeof jv === _$_543c[2]) {
                            jx = jv
                        }
                    }
                    ;iP.sign = iJ(jx);
                    iP.cts = new Date().getTime();
                    jw = iI(iP);
                    if (Rohr_Opt.LogVal && typeof (window) !== _$_543c[0]) {
                        window[Rohr_Opt.LogVal] = encodeURIComponent(jw)
                    }
                    ;return jw
                }

'''
def deal_text(href,code):
    code_first_two=code[0:2]
    r=requests.get(url=href,headers=headers)
    '''获取偏移量'''
    jvguv=re.findall('%s{background:-(.*?).0px -(.*?).0px;}'%code,r.text)
    x=int(jvguv[0][0])
    y=int(jvguv[0][1])
    '''获取加密的汉字'''
    url='https:'+re.findall(r'svgmtsi\[class\^="%s"].*?background-image: url\((.*?)\)'%code_first_two,r.text)[0]
    num=requests.get(url=url,headers=headers)
    q=re.findall('y="(\d+)"',num.text)
    tree=etree.HTML(num.content)
    y1=int(q[0])
    y2=int(q[1])
    y3=int(q[2])
    y4=int(q[3])
    y5=int(q[4])
    a=tree.xpath('//text[@y="%s"]/text()'%y1)[0]
    b=tree.xpath('//text[@y="%s"]/text()'%y2)[0]
    c=tree.xpath('//text[@y="%s"]/text()'%y3)[0]
    d= tree.xpath('//text[@y="%s"]/text()'%y4)[0]
    e= tree.xpath('//text[@y="%s"]/text()'%y5)[0]
    if  y<y1 :
        text=a[x // 12]
    elif y<y2:
        text= b[x // 12]
    elif y<y3 :
        text = c[x // 12]
    elif y<y4 :
        text = d[x // 12]
    else:
        text= e[x //12]
    return text
def deal_num(href,code):
    code_first_two=code[0:2]
    r=requests.get(url=href,headers=headers)
    '''获取偏移量'''
    jvguv=re.findall('%s{background:-(.*?).0px -(.*?).0px;}'%code,r.text)
    x=int(jvguv[0][0])
    y=jvguv[0][1]
    '''获取加密的数字'''
    url='https:'+re.findall(r'svgmtsi\[class\^="%s"].*?background-image: url\((.*?)\)'%code_first_two,r.text)[0]
    num=requests.get(url=url,headers=headers)
    q=re.findall('y="(\d+)"',num.text)
    tree=etree.HTML(num.content)
    y1=q[0]
    y2=q[1]
    y3=q[2]
    a=tree.xpath('//text[@y="%s"]/text()'%y1)[0]
    b=tree.xpath('//text[@y="%s"]/text()'%y2)[0]
    c=tree.xpath('//text[@y="%s"]/text()'%y3)[0]
    if y<=y1:
        return a[x//12]
    elif y<=y2:
        return b[x // 12]
    else :
        return c[x // 12]


def get_shopcode():
    while True :
        try:
            r=requests.get(url='http://www.dianping.com/huizhou/ch10/g103',headers=headers)
            text=r.text
            tree = etree.HTML(text)
            href = 'http://s3plus' + re.findall('//s3plus(.*?)">', text)[0]
            shops = tree.xpath('.//div[@id="shop-all-list"]/ul/li')
            for shop in shops :
                a = ''
                c = ''
                d=''
                shop_name = shop.xpath('.//div[@class="tit"]/a/h4/text()')[0]
                star = shop.xpath('.//div[@class="comment"]/span')[0]
                review_num = shop.xpath('.//div[@class="comment"]/a[contains(@class,"review-num")]/b')[0]  # 获取可见的数字

                review_num1 = shop.xpath('.//div[@class="comment"]/a[contains(@class,"mean-price")]/b')[0]
                tag = shop.xpath('.//div[@class="tag-addr"]/a[2]/span')[0]
                addr = shop.xpath('.//div[@class="tag-addr"]//span')[0]


                addr_text = shop.xpath('.//div[@class="operate J_operate Hide"]/a[2]')[0]
                '''获取标签下所有的text'''
                # print(addr_text.xpath('string(.)'))
                star = star.attrib['title']
                for i in review_num1 :
                    code = i.attrib['class']
                    b = deal_num(href, code)
                    c = c + b
                for i in review_num :

                    code = i.attrib['class']
                    b = deal_num(href, code)
                    a = a + b
                    # print(i.attrib['class'])
                # for i in tag :
                #     print(i.attrib['class'])
                # if addr.text:
                #     print("123")
                # for i in addr:
                #     text = i.attrib['class']
                #     b = deal_text(href,text)
                #     d = d + b
                # print(d)
                print(addr_text.attrib['data-address'])
                print(star + '  ' + shop_name + '  ' + a + '条点评' + '  ' + '人均' + c)
                print('-------------------------')

            break
        except  Exception as e:
            pass
get_shopcode()
# for i in range(0,len(comment)):
#
#     shanghu.append(comment[i])
# print(comment)

