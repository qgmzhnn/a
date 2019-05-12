import hashlib
import time
import random
import requests
import json
headers = {
    'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19',
    # 'Accept':'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Encoding':'gzip, deflate',
    # 'Accept-Language':'zh-CN,zh;q=0.9',
    # 'Connection':'keep-alive',
    # 'Content-Length':'242',
    # 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    #  'X-Requested-With': 'XMLHttpRequest',
    # 'Cookie':'OUTFOX_SEARCH_USER_ID=1815009121@10.169.0.84; JSESSIONID=aaaA5zmPB9trAbewFlzPw; OUTFOX_SEARCH_USER_ID_NCOO=647597625.4547813; ___rl__test__cookies=1556274873468',
    # 'Host':'fanyi.youdao.com',
    # 'Origin':'http://fanyi.youdao.com',
    # 'Referer':'http://fanyi.youdao.com/',

}
def get_data():
    r="5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    hash=hashlib.md5()
    hash.update(r.encode('utf-8'))
    bv=hash.hexdigest()
    ts=str(int(time.time()*1000))
    ran=str(random.randint(0,10))
    salt=ts+ran
    text='fanyideskweb'+"FY_BY_REALTlME"+ran+"@6f#X3=cCuncYssPsuRUE"
    hash.update(text.encode('utf-8'))
    sign=hash.hexdigest()
    data={
        'i' : input("请输入"),
        'from ' : "AUTO",
        'to' : "AUTO",
        'smartresult' : "dict",
        'client' : 'fanyideskweb',
        'salt' : salt,
        'sign' : sign,
        'ts' : ts,
        'bv' : bv,
        'doctype' : 'json',
        'version' : '2.1',
        'keyfrom' : 'fanyi.web',
        'action' : "FY_BY_DEFAULT",

    }
    return data
def main():
    data=get_data()
    r=requests.post(url='http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule',headers=headers,data=data)
    print(json.loads(r.text)['translateResult'][0][0]['tgt'])
    print(r.text)

if __name__ == '__main__':
    main()
