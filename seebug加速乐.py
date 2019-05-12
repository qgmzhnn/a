import requests
import re
import json
import execjs
import time
import os
os.environ["EXECJS_RUNTIME"]="Node"
#先get网页，得到一个加密的js代码1，解密后得到另外一个js代码2，运行代码2，会得到一个 __jsl_clearance ，用 __jsl_clearance
#作为cookie再去get网页并且记录第二次get得到的cookie __jsluid， 会得到加密js代码3，解密后的得到js代码4，运行代码4，会得到最终的 __jsl_clearance
#将第二次记录下的__jsluid和通过运行js代码4得到的__jsl_clearance 作为cookie再次get网页，即可成功！！！！！
a=''
headers={
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',

}
head='''
    var window = {};
    window.document = {body:{innerHTML:"1"}, documentElement:{attributes:{webdriver:"1"}}, createElement:function(x){return {innerHTML:"1"}}};
    var document = window.document;  

'''
window='''
 var window={}
'''
def get_js():
    f = open(r'C:\Users\cy\Desktop\seebug.js', 'r', encoding='utf-8')

    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr
def get_one(text):
    while True:
        try :
            print(text)
            text = re.findall('<script>(.*?)</script>', text)[0].replace('eval(', 'return(')
            # with open('C:\Users\cy\Desktop\seebug.js','w') as f:
            #     f.write(str(text[0]))
            jsstr = "function y(){" + text + "};"
            ctx = execjs.compile(jsstr)
            __jsl_clearance = ctx.call('y')
            a = re.findall('var(.*?)=function', __jsl_clearance)[0]
            __jsl_clearance = __jsl_clearance.replace('document.cookie=', 'return ')
            __jsl_clearance = head + 'var' + a + '=function(){return' + re.findall('return(.*)};', __jsl_clearance)[ 0] + '};'
            ctx = execjs.compile(__jsl_clearance)
            __jsl_clearance = ctx.call(a)
            print(__jsl_clearance)
            __jsl_clearance = re.findall('__jsl_clearance=(.*?);', __jsl_clearance)[0]
            return __jsl_clearance
        except Exception as e:
          exit()
def set_cookies(s,text):
    __jsl_clearance = get_one(text)
    print(__jsl_clearance)
    # exit()
    # print(str(__jsl_clearance)[0:28])
    new_headers={
        'Cookie':'__jsl_clearance=%s'%__jsl_clearance,
        #     'Cookie':'__jsluid=8817f1e029e5c8cd7220c03c730f348c;__jsl_clearance=1554896988.334|0|Z1mbpX5roEaRhMQz21QMXoD4084%3D',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    r = s.get(url='https://www.seebug.org/vuldb/ssvid-97922',headers=new_headers)
    text=r.text
    cookie = r.cookies['__jsluid']
    print(cookie)
    __jsl_clearance=get_one(text)
    print(__jsl_clearance)
    new_headers2={
        'Cookie':'__jsluid=%s'%cookie+';'+'__jsl_clearance=%s' % __jsl_clearance,
        'Content-Type': 'application/json;charset=UTF-8',
        'X - Requested - With' : 'XMLHttpRequest',
        'Accept - Encoding' : 'gzip, deflate',
        'Accept - Language' : 'zh - CN, zh;q = 0.9',

    #     'Cookie':'__jsluid=8817f1e029e5c8cd7220c03c730f348c;__jsl_clearance=1554896988.334|0|Z1mbpX5roEaRhMQz21QMXoD4084%3D',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    }
    #payload数据为json格式，使用jsom.dumps转为json并提交
    payload = {
        'currentPage' : 1,
        'filter' : {'title' : '',
                    'number' : '',
                    'province' : '',
                    'pid' : '',
                    'buyer' : '',
                    'agency' : ''},
        'str' : '无,无,近一周',
    }
    payload = json.dumps(payload)
    r = s.get(url='https://www.seebug.org/vuldb/ssvid-97922', headers=new_headers2)
    print(r.text)
    print(r.status_code)
    # r=s.post(url='http://www.cyicai.com/information/applyForSubscriptionList',headers=new_headers2,data=payload)
    #
    #
    #
    # print(r.text)
    # print(r.cookies)
    # print(r.status_code)
def main():
    s=requests.session()
    text=s.get(url='https://www.seebug.org/vuldb/ssvid-97922',headers=headers).text
    set_cookies(s,text)
if __name__ == '__main__':
    main()
