import requests
from lxml import etree
import urllib
import execjs
from Crypto.Cipher import AES
import random
import math
import hashlib
import binascii
import base64
import rsa
import time
import urllib3
import execjs
import re
import os
os.environ["EXECJS_RUNTIME"]="Node"
a=''
b=''
UM_DISTINCTID=''
s = requests.Session()
encryptPassChars ='0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz*&-%/!?*+=()'
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',

}
def get_js():
    f = open(r'C:\Users\yuanbaba\Desktop\eval.js', 'r', encoding='utf-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr
def create_data(password,csrf):
    data = {

        'username' : '3106614875@qq.com',
        'password' :'mXj8x2AItMan4DKtpUVRVAU1zCrCFPUQi3IOHI7SiWR7hCNK6TwwjIDRj9LuyS20DZ3RpeLzQaBHnClt2nYTJ8AkwGWov13m+Gp1bz9Zm+qQJAI3dWTjY5DG96zHYZj/PbnGF9ETIufWaXr5e9vl2usIQK62ShUXXiX2mRx2U0F5BYdEh7JM3P+OoMliAyx6Sk30eMAJ04+bIbtjBKz0VxGMMe/vacYjzGY2UGGtm/e0fXqNr0kPV3mmxrHcrdFkzkaKaP6CWwyNjSyXtEpJiZbkEA+UoQTDrUkQWYBi0wxIjVNOUY6KWT/+/28takN5vfWTrKGpuAgiFik0J8rVgw==:::fT4XjBEZ2KYwiyjKRm+tkg==',
        '_spring_security_remember_me' : 'true',
        '_csrf' :csrf,
    }
    return  data

def ranstr(num):
    a='abcdefghijklmnopqrstuvwxyz0123456789'
    str=''
    for i in range(0,num):
        str+=random.choice(a)
    # print(str)
    return str
def generateEncryptPassword():
    randomstring=''
    for i in range(0,32):
        rnum=math.floor(random.random()*len(encryptPassChars))
        randomstring+=encryptPassChars[rnum:rnum+1]
    # print(randomstring)
    return randomstring
def keyEncrypt():
    passPhrase = generateEncryptPassword()
    salt=ranstr(32)
    iv=ranstr(16)
    key=hashlib.pbkdf2_hmac("md5",bytes(passPhrase,encoding='utf-8'),bytes(salt,encoding='utf-8'),iterations=1000,dklen=16)
    key=binascii.hexlify(key).decode()
    # print(key)
    # print(len(key))
    # exit()
    # print(binascii.hexlify(key).decode())
    BS = AES.block_size
    # 加密算法
    pad = lambda s : s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
    text = str(pad('yuan1998'))
    encryptor = AES.new(str.encode(key),AES.MODE_CBC,str.encode(iv))
    msg = encryptor.encrypt(bytes(text, 'utf-8'))
    aesEncrypted = str(base64.encodebytes(msg), encoding='utf-8')
    global b
    for i in aesEncrypted:
        if i!='\n':
            b=b+i

    aesKey = passPhrase + ":::" + salt + ":::" + iv
    # (public_key,private_key)=rsa.newkeys(1024)
    # with open(r'C:\Users\yuanbaba\Desktop\public1.pem', 'wb') as file :
    #     file.write(public_key.save_pkcs1())
    # exit()
    with open(r'C:\Users\cy\Desktop\public1.pem','rb') as file:
        p=file.read()
        publicKey=rsa.PublicKey.load_pkcs1_openssl_pem(p)
    rsaKey = rsa.encrypt(bytes(aesKey,encoding='utf-8'), publicKey)
    rsaKey=str(base64.encodebytes(rsaKey), encoding='utf-8')
    for i in rsaKey:
        global a
        if i!='\n':
            a = a + i
    # print(a + ":::" + b)
    return a + ":::" + b
    # return b
def get_msg():
    r = s.get(url='http://openlaw.cn/login.jsp', headers=headers)
    tree = etree.HTML(r.text)
    _csrf = tree.xpath('//form[@class="wpcf7-form"]/input/@value')
    csrf =_csrf[0]
    data=create_data(keyEncrypt(),csrf)
    r=s.post(url='http://openlaw.cn/login',headers=headers,data=data)
    r = s.get(url='http://openlaw.cn/judgement/7df2b3aced854bb8964e78a2737b58a5', headers=headers)


    return r.text

def deal_text():
    text=get_msg()
    print(text)
    data=re.findall('eval(.*)',text)
    data='function eval(){'+str(data).replace("['([]",'return ').replace("())']",'')+'}'
    ctx = execjs.compile(data)
    data = str(ctx.call('eval')).replace('\\','').replace('[','').replace(']','')
    OPEN2='OPEN'+str(re.findall('OPEN(.*)_process',data)).replace('["','').replace('"]','').replace("='+",'')
    c=str(re.findall('document.cookie=(.*)if',data)).replace('document.cookie=','')
    SIGNIN_ID='SIGNIN_ID='+str(re.findall('SIGNIN_ID=(.*)SIGNIN_UC',c)).replace('"','').replace('[','').replace(';','').replace("'",'').replace(']','')+';'
    SIGNIN_UC='SIGNIN_UC='+str(re.findall('SIGNIN_UC=(.*)UNDEFINED',c)).replace('"','').replace('[','').replace(';','').replace("'",'').replace(']','')+';'
    UNDEFINED='UNDEFINED='+str(re.findall('UNDEFINED=(.*)',c)).replace('"','').replace('[','').replace(']','').replace("'",'').replace('\\','').replace(';','')+';'
    print(SIGNIN_ID)
    print(SIGNIN_UC)
    print(UNDEFINED)
    _process='function _process'+str(re.findall('function _process(.*)var _switch',data)).replace('\\','').replace('"','').replace('[','').replace(']','').replace('};','')+'}'

    with open('openlaw.txt','w',encoding='utf-8') as file:
        file.write(text)
    with open('openlaw.txt', 'r') as file:
        a=file.readline()
        print(a)
        for i in range(0,100):
            if a[0:1]=='$':
                a = 'function a(){'+str(a).replace('$.$($.$(','return ').replace(')())();','')+'}'
                ctx=execjs.compile(a)
                a=ctx.call('a')
                a='function b(){'+a+'}'
                ctx=execjs.compile(a)
                a=str(ctx.call('b')).replace('document.cookie=','')
                a=str(re.findall('{(.*?)}',a))
                # a=list(a)
                OPEN_ID = 'OPEN_ID'+str(re.findall('OPEN_ID(.*)',a)).replace('"','').replace('[','').replace(']','').replace("'",'').replace('\\','')+';'
                print(OPEN_ID)
                OPEN='OPEN'+str(re.findall('OPEN(.*?)OPEN',a)).replace('"','').replace('[','').replace(']','').replace("'",'')
                # exit()
                UM_DISTINCTID='UM_DISTINCTID'+str(re.findall('UM_DISTINCTID(.*?)]',a)).replace('"','').replace('[','').replace(']','').replace("'",'').replace('\\','')+';'
                UM_DISTINCTID='UM_DISTINCTID='+str(re.findall('\d+',UM_DISTINCTID)).replace('[','').replace(']','').replace("'",'')+';'
                code=str(re.findall('=+(.*);',OPEN)).replace("['+",'').replace("']",'')
                print(OPEN_ID)
                # print(type(a))
                break
            a = file.readline()
        file.close()
    var=get_var(text,code)
    OPEN='OPEN'+str(re.findall('OPEN(.*)=',OPEN)).replace("['",'').replace("']",'')+'='+var+';'
    ctx = execjs.compile(_process)
    data =OPEN2+'='+str(ctx.call('_process',var))+';'
    print(data)
    cookies={
        'Cookie':SIGNIN_ID+SIGNIN_UC+UNDEFINED+OPEN_ID+OPEN+data
    }


    return cookies
def get_var(text,var):
    s = var
    for i in text:

        a = re.findall('var %s .*'%s, text)
        if len(a) != 0:
            a = ''.join(a[0])
            a = re.findall('"' '.*''"', a)
            a = ''.join(a[0])
            a=eval(a)
            return a
def send_cookie():
    cookies=deal_text()
    r = s.get(url='http://openlaw.cn/judgement/7df2b3aced854bb8964e78a2737b58a5', headers=headers,cookies=cookies)
    print(r.text)
def main():
    send_cookie()
if __name__ == '__main__':
    main()
